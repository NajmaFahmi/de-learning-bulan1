import great_expectations as gx
import pandas as pd
from src.logger import get_logger 


## 1. Define logger
logger = get_logger("ge_validator")


## 2. Validate data using GE
def validate_flights_data(df: pd.DataFrame) -> bool:
    """
    Validasi kewajaran bisnis data flight SEBELUM masuk ke Pydantic.
    Return True kalau lolos, False kalau ada yg tidak lolos.
    """
    logger.info("Running Great Expectations validation...")

    # Setup GE context
    context = gx.get_context()

    # Buat data source dari dataframe
    data_source = context.data_sources.add_pandas("airlines_source")
    data_asset = data_source.add_dataframe_asset("flights_table")
    batch_def = data_asset.add_batch_definition_whole_dataframe("batch_flights")
    batch = batch_def.get_batch(batch_parameters={"dataframe": df})

    # Buat suite
    suite = context.suites.add(
        gx.ExpectationSuite(name="aturan_bisnis_flights")
    )

    # Buat aturan (expectations)
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="Month", min_value=1, max_value=12
        )
    )       # bulan harus 1 - 12

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="ArrDelay", min_value=-120, max_value=1440
        )
    )       # delay tidak boleh lebih dari 24 jam (1140 mins)
            # atau kurang dari -120 menit lebih awal

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="Cancelled", value_set=[0,1]
        )
    )

    # Jalankan test / validasi
    validation_def = context.validation_definitions.add(
        gx.ValidationDefinition(
            name="cek_bisnis_flights",
            data=batch_def,
            suite=suite
        )
    )

    # Simpan hasilnya
    results = validation_def.run(batch_parameters={"dataframe": df})

    # Log hasilnya
    stats = results.statistics
    logger.info(
        f"GE Validation: {stats['successful_expectations']}/{stats['evaluated_expectations']} rule passed"
    )

    # ## Jika ada error & tidak berhasil --> BLOKIR SEPENUHNYA:
    # if not results.success:
    #     logger.error("GE Validation FAILED - data korup ditemukan sebelum masuk pipeline")
    #     for result in results.results:
    #         if not result.success:
    #             logger.error(
    #                 f"GAGAL: {result.expectation_config.type} "
    #                 f"pada kolom '{result.expectation_config.kwargs.get('column')}"
    #                 f"- {result.result.get('unexpected_count', 0)} nilai bermasalah"
    #             )
    #     return False 
    
    # logger.info("GE Validation PASSED -- data aman dilanjutkan ke Pydantic.")
    # return True

    ## Jika ada error & tidak berhasil --> cek berapa data yg error
    ## Kalau < 1% dari total data maka tetap JALANKAN, jika lebih BLOKIR
    THRESHOLD = 1.0

    if not results.success:
        for result in results.results:
            if not result.success:
                unexpected_percent = result.result.get('unexpected_percent', 0)
                col = result.expectation_config.kwargs.get('column')
                count = result.result.get('unexpected_count', 0)

                if unexpected_percent > THRESHOLD:
                    logger.error(
                        f"FATAL: kolom '{col}' -- {count} nilai bermasalah "
                        f"({unexpected_percent:.2f}%) -- melebihi threshold {THRESHOLD}"
                    )
                    return False 
                else:
                    logger.warning(
                        f"MINOR: kolom '{col}' -- {count} nilai bermasalah "
                        f"({unexpected_percent:.4f}%) -- di bawah threshold, pipeline dilanjutkan"
                    )

    logger.info("GE Validation selesai -- pipeline dilanjutkan ke Pydantic")
    return True