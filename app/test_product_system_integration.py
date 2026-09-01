# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# PRODUCT SYSTEM INTEGRATION TEST
#
# Tests:
#   product_engine
#   library_store
#   product_ui
#   product_management_ui
#
# Product lifecycle:
#
# CREATE → STORE → READ → UPDATE → SEARCH → DELETE → VERIFY
# ==========================================================

import streamlit as st
import traceback
import uuid


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Product System Integration Test",
    page_icon="🧪",
    layout="wide",
)


# ==========================================================
# TITLE
# ==========================================================

st.title("🧪 Product System Integration Test")

st.caption(
    "Solar PV Designer Pro Africa™ — Product Library "
    "backend and UI integration diagnostic"
)


# ==========================================================
# TEST RESULTS
# ==========================================================

results = []


def record_result(
    test_name,
    success,
    message,
):
    results.append(
        {
            "test": test_name,
            "success": success,
            "message": message,
        }
    )


# ==========================================================
# IMPORT TESTS
# ==========================================================

st.header("1. Module Import Tests")


# ----------------------------------------------------------
# library_store
# ----------------------------------------------------------

try:

    import library_store

    record_result(
        "library_store import",
        True,
        "library_store.py imported successfully.",
    )

except Exception as exc:

    library_store = None

    record_result(
        "library_store import",
        False,
        f"{type(exc).__name__}: {exc}",
    )


# ----------------------------------------------------------
# product_engine
# ----------------------------------------------------------

try:

    import product_engine

    record_result(
        "product_engine import",
        True,
        "product_engine.py imported successfully.",
    )

except Exception as exc:

    product_engine = None

    record_result(
        "product_engine import",
        False,
        f"{type(exc).__name__}: {exc}",
    )


# ----------------------------------------------------------
# product_ui
# ----------------------------------------------------------

try:

    import product_ui

    record_result(
        "product_ui import",
        True,
        "product_ui.py imported successfully.",
    )

except Exception as exc:

    product_ui = None

    record_result(
        "product_ui import",
        False,
        f"{type(exc).__name__}: {exc}",
    )


# ----------------------------------------------------------
# product_management_ui
# ----------------------------------------------------------

try:

    import product_management_ui

    record_result(
        "product_management_ui import",
        True,
        "product_management_ui.py imported successfully.",
    )

except Exception as exc:

    product_management_ui = None

    record_result(
        "product_management_ui import",
        False,
        f"{type(exc).__name__}: {exc}",
    )


# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

st.header("2. Database Initialization")


if library_store is not None:

    try:

        initialized = library_store.initialize_database()

        record_result(
            "SQLite database initialization",
            bool(initialized),
            (
                "Database initialized successfully."
                if initialized
                else "Database initialization returned False."
            ),
        )

    except Exception as exc:

        record_result(
            "SQLite database initialization",
            False,
            f"{type(exc).__name__}: {exc}",
        )

else:

    record_result(
        "SQLite database initialization",
        False,
        "library_store.py could not be imported.",
    )


# ==========================================================
# DATABASE LOCATION
# ==========================================================

if library_store is not None:

    st.subheader("Database Location")

    database_file = getattr(
        library_store,
        "DATABASE_FILE",
        None,
    )

    if database_file is None:

        database_file = getattr(
            library_store,
            "DB_PATH",
            None,
        )

    if database_file is not None:

        st.code(
            str(database_file)
        )

        try:

            exists = database_file.exists()

        except Exception:

            exists = False

        if exists:

            st.success(
                "Database file exists."
            )

        else:

            st.warning(
                "Database file does not currently exist."
            )


# ==========================================================
# INITIAL PRODUCT COUNT
# ==========================================================

st.header("3. Initial Product Library State")


initial_products = []


if library_store is not None:

    try:

        initial_products = (
            library_store.load_product_library()
        )

        if initial_products is None:

            initial_products = []

        st.write(
            f"Products currently in SQLite: "
            f"**{len(initial_products)}**"
        )

        if initial_products:

            st.info(
                "Existing products were found. "
                "The integration test will use a unique "
                "temporary test product and will not delete "
                "existing products."
            )

        else:

            st.info(
                "The SQLite product library is currently empty."
            )

    except Exception as exc:

        record_result(
            "Initial product load",
            False,
            f"{type(exc).__name__}: {exc}",
        )

else:

    st.error(
        "library_store.py is unavailable."
    )


# ==========================================================
# CREATE UNIQUE TEST PRODUCT
# ==========================================================

st.header("4. Product Lifecycle Test")


test_id = (
    "integration_test_"
    + uuid.uuid4().hex[:12]
)


test_product = {

    "id": test_id,

    "name":
        "Integration Test Solar Panel",

    "category":
        "Solar Panel",

    "manufacturer":
        "Solar PV Designer Pro",

    "model":
        "INTEGRATION-TEST-550W",

    "technology":
        "Monocrystalline",

    "rated_power_w":
        550,

    "voltage_v":
        41.5,

    "current_a":
        13.2,

    "efficiency_percent":
        21.5,

    "warranty_years":
        10,

    "price":
        150,

    "currency":
        "USD",

    "quantity":
        1,

    "notes":
        "Temporary product created by "
        "test_product_system_integration.py",

    "capacity_ah":
        0,

    "energy_kwh":
        0,

    "supplier":
        "Integration Test Supplier",

    "country":
        "Uganda",

    "specifications": {

        "cell_type":
            "N-type",

        "test_product":
            True,

        "test_version":
            "integration",

    },
}


# ==========================================================
# STEP 1 — CREATE
# ==========================================================

st.subheader("4.1 CREATE — Add test product")


created_product = None


if library_store is not None:

    try:

        created_product = (
            library_store.add_product_to_library(
                test_product
            )
        )

        if created_product:

            record_result(
                "CREATE product",
                True,
                (
                    "Test product created successfully "
                    f"with ID: {test_id}"
                ),
            )

            st.success(
                "Test product created successfully."
            )

        else:

            record_result(
                "CREATE product",
                False,
                "add_product_to_library returned no product.",
            )

    except Exception as exc:

        record_result(
            "CREATE product",
            False,
            f"{type(exc).__name__}: {exc}",
        )

        st.error(
            f"CREATE failed: {exc}"
        )

else:

    record_result(
        "CREATE product",
        False,
        "library_store.py unavailable.",
    )


# ==========================================================
# STEP 2 — READ
# ==========================================================

st.subheader("4.2 READ — Retrieve test product")


retrieved_product = None


if library_store is not None:

    try:

        if hasattr(
            library_store,
            "get_product_from_library",
        ):

            retrieved_product = (
                library_store.get_product_from_library(
                    test_id
                )
            )

        else:

            products = (
                library_store.load_product_library()
            )

            for product in products:

                if str(
                    product.get("id")
                ) == test_id:

                    retrieved_product = product

                    break


        if retrieved_product:

            record_result(
                "READ product",
                True,
                "Test product retrieved successfully.",
            )

            st.success(
                "Test product retrieved successfully."
            )

            with st.expander(
                "View retrieved product"
            ):

                st.json(
                    retrieved_product
                )

        else:

            record_result(
                "READ product",
                False,
                "Test product could not be retrieved.",
            )

            st.error(
                "Test product was not found after creation."
            )

    except Exception as exc:

        record_result(
            "READ product",
            False,
            f"{type(exc).__name__}: {exc}",
        )

        st.error(
            f"READ failed: {exc}"
        )

else:

    record_result(
        "READ product",
        False,
        "library_store.py unavailable.",
    )


# ==========================================================
# STEP 3 — UPDATE
# ==========================================================

st.subheader("4.3 UPDATE — Modify test product")


updated_product = None


if library_store is not None:

    try:

        update_data = {

            "name":
                "Integration Test Solar Panel UPDATED",

            "price":
                175,

            "quantity":
                2,

            "notes":
                "Product successfully updated "
                "during integration testing.",

        }


        if hasattr(
            library_store,
            "update_product_in_library",
        ):

            update_success = (
                library_store.update_product_in_library(
                    test_id,
                    update_data,
                )
            )

        else:

            update_success = False


        if update_success:

            record_result(
                "UPDATE product",
                True,
                "Test product updated successfully.",
            )

            st.success(
                "Test product updated successfully."
            )


            if hasattr(
                library_store,
                "get_product_from_library",
            ):

                updated_product = (
                    library_store.get_product_from_library(
                        test_id
                    )
                )


            if updated_product:

                st.write(
                    "Updated values:"
                )

                st.json(
                    {
                        "name":
                            updated_product.get(
                                "name"
                            ),

                        "price":
                            updated_product.get(
                                "price"
                            ),

                        "quantity":
                            updated_product.get(
                                "quantity"
                            ),
                    }
                )

        else:

            record_result(
                "UPDATE product",
                False,
                "Product update returned False.",
            )

            st.error(
                "Product update failed."
            )

    except Exception as exc:

        record_result(
            "UPDATE product",
            False,
            f"{type(exc).__name__}: {exc}",
        )

        st.error(
            f"UPDATE failed: {exc}"
        )

else:

    record_result(
        "UPDATE product",
        False,
        "library_store.py unavailable.",
    )


# ==========================================================
# STEP 4 — SEARCH
# ==========================================================

st.subheader("4.4 SEARCH — Find test product")


search_results = []


if library_store is not None:

    try:

        if hasattr(
            library_store,
            "search_product_library",
        ):

            search_results = (
                library_store.search_product_library(
                    "Integration Test Solar Panel"
                )
            )

        else:

            products = (
                library_store.load_product_library()
            )

            search_results = [

                product

                for product in products

                if "Integration Test Solar Panel"
                in str(
                    product.get(
                        "name",
                        ""
                    )
                )

            ]


        if search_results:

            record_result(
                "SEARCH product",
                True,
                (
                    "Search successfully found "
                    f"{len(search_results)} test product(s)."
                ),
            )

            st.success(
                f"Search found {len(search_results)} test product(s)."
            )

            st.json(
                search_results
            )

        else:

            record_result(
                "SEARCH product",
                False,
                "Search returned no matching product.",
            )

            st.error(
                "Search could not find the test product."
            )

    except Exception as exc:

        record_result(
            "SEARCH product",
            False,
            f"{type(exc).__name__}: {exc}",
        )

        st.error(
            f"SEARCH failed: {exc}"
        )

else:

    record_result(
        "SEARCH product",
        False,
        "library_store.py unavailable.",
    )


# ==========================================================
# STEP 5 — PRODUCT UI READ
# ==========================================================

st.subheader("4.5 PRODUCT UI — Verify library visibility")


if product_ui is not None:

    try:

        if hasattr(
            product_ui,
            "get_products",
        ):

            ui_products = (
                product_ui.get_products()
            )

            if ui_products is None:

                ui_products = []


            matching_ui_products = [

                product

                for product in ui_products

                if str(
                    product.get(
                        "id",
                        ""
                    )
                ) == test_id

            ]


            if matching_ui_products:

                record_result(
                    "product_ui visibility",
                    True,
                    (
                        "product_ui.get_products() "
                        "can see the test product."
                    ),
                )

                st.success(
                    "product_ui.py can see the test product."
                )

            else:

                record_result(
                    "product_ui visibility",
                    False,
                    (
                        "product_ui.get_products() "
                        "cannot see the test product."
                    ),
                )

                st.warning(
                    "product_ui.py did not return the test product."
                )

        else:

            record_result(
                "product_ui visibility",
                False,
                "product_ui.get_products() is unavailable.",
            )

    except Exception as exc:

        record_result(
            "product_ui visibility",
            False,
            f"{type(exc).__name__}: {exc}",
        )

else:

    record_result(
        "product_ui visibility",
        False,
        "product_ui.py unavailable.",
    )


# ==========================================================
# STEP 6 — MANAGEMENT UI MODULE
# ==========================================================

st.subheader(
    "4.6 PRODUCT MANAGEMENT UI — Module verification"
)


if product_management_ui is not None:

    required_functions = [

        "display_product_management_ui",

    ]


    missing_functions = [

        function_name

        for function_name in required_functions

        if not hasattr(
            product_management_ui,
            function_name,
        )

    ]


    if not missing_functions:

        record_result(
            "product_management_ui structure",
            True,
            (
                "Required management UI function "
                "is available."
            ),
        )

        st.success(
            "Product Management UI structure is valid."
        )

    else:

        record_result(
            "product_management_ui structure",
            False,
            (
                "Missing functions: "
                + ", ".join(
                    missing_functions
                )
            ),
        )

        st.error(
            "Missing Product Management UI functions."
        )

else:

    record_result(
        "product_management_ui structure",
        False,
        "product_management_ui.py unavailable.",
    )


# ==========================================================
# STEP 7 — DELETE
# ==========================================================

st.subheader("4.7 DELETE — Remove temporary test product")


delete_success = False


if library_store is not None:

    try:

        if hasattr(
            library_store,
            "remove_product_from_library",
        ):

            delete_success = (
                library_store.remove_product_from_library(
                    test_id
                )
            )


        if delete_success:

            record_result(
                "DELETE product",
                True,
                "Temporary test product deleted successfully.",
            )

            st.success(
                "Temporary test product deleted successfully."
            )

        else:

            record_result(
                "DELETE product",
                False,
                "Product deletion returned False.",
            )

            st.error(
                "Temporary test product could not be deleted."
            )

    except Exception as exc:

        record_result(
            "DELETE product",
            False,
            f"{type(exc).__name__}: {exc}",
        )

        st.error(
            f"DELETE failed: {exc}"
        )

else:

    record_result(
        "DELETE product",
        False,
        "library_store.py unavailable.",
    )


# ==========================================================
# STEP 8 — VERIFY DELETION
# ==========================================================

st.subheader(
    "4.8 VERIFY DELETE — Confirm test product is gone"
)


if library_store is not None:

    try:

        remaining_product = None


        if hasattr(
            library_store,
            "get_product_from_library",
        ):

            remaining_product = (
                library_store.get_product_from_library(
                    test_id
                )
            )

        else:

            products = (
                library_store.load_product_library()
            )

            for product in products:

                if str(
                    product.get(
                        "id"
                    )
                ) == test_id:

                    remaining_product = product

                    break


        if remaining_product is None:

            record_result(
                "VERIFY DELETE",
                True,
                (
                    "Test product is no longer "
                    "present in the database."
                ),
            )

            st.success(
                "Deletion verified — test product is gone."
            )

        else:

            record_result(
                "VERIFY DELETE",
                False,
                (
                    "Test product still exists "
                    "after deletion."
                ),
            )

            st.error(
                "Deletion verification failed."
            )

    except Exception as exc:

        record_result(
            "VERIFY DELETE",
            False,
            f"{type(exc).__name__}: {exc}",
        )

else:

    record_result(
        "VERIFY DELETE",
        False,
        "library_store.py unavailable.",
    )


# ==========================================================
# FINAL DATABASE STATE
# ==========================================================

st.header("5. Final Product Library State")


if library_store is not None:

    try:

        final_products = (
            library_store.load_product_library()
        )

        if final_products is None:

            final_products = []


        st.metric(
            "Products Remaining",
            len(final_products),
        )


        if final_products:

            st.write(
                "Existing products were preserved:"
            )

            st.dataframe(
                final_products,
                use_container_width=True,
            )

        else:

            st.info(
                "No products remain in the library."
            )

    except Exception as exc:

        st.error(
            f"Could not load final product library: {exc}"
        )


# ==========================================================
# FINAL TEST SUMMARY
# ==========================================================

st.header("6. Integration Test Summary")


passed = sum(
    1
    for result in results
    if result["success"]
)


failed = sum(
    1
    for result in results
    if not result["success"]
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Tests Passed",
        passed,
    )


with col2:

    st.metric(
        "Tests Failed",
        failed,
    )


with col3:

    st.metric(
        "Total Tests",
        len(results),
    )


# ==========================================================
# RESULT TABLE
# ==========================================================

st.subheader("Detailed Results")


for result in results:

    if result["success"]:

        st.success(
            f"✅ {result['test']} — "
            f"{result['message']}"
        )

    else:

        st.error(
            f"❌ {result['test']} — "
            f"{result['message']}"
        )


# ==========================================================
# FINAL STATUS
# ==========================================================

if failed == 0:

    st.success(
        "🎉 PRODUCT SYSTEM INTEGRATION TEST PASSED"
    )

    st.write(
        """
        The product system successfully completed the
        product lifecycle:

        CREATE → STORE → READ → UPDATE → SEARCH →
        UI VISIBILITY → DELETE → VERIFY DELETE
        """
    )

else:

    st.warning(
        "⚠️ PRODUCT SYSTEM INTEGRATION TEST COMPLETED "
        "WITH FAILURES"
    )

    st.write(
        "Review the failed tests above before proceeding "
        "to the final main.py integration."
    )


# ==========================================================
# DEBUG INFORMATION
# ==========================================================

with st.expander(
    "Developer Debug Information"
):

    st.write(
        "Temporary test product ID:"
    )

    st.code(
        test_id
    )

    st.write(
        "Python module locations:"
    )

    if library_store is not None:

        st.write(
            "library_store.py:"
        )

        st.code(
            str(
                getattr(
                    library_store,
                    "__file__",
                    "Unknown",
                )
            )
        )


    if product_engine is not None:

        st.write(
            "product_engine.py:"
        )

        st.code(
            str(
                getattr(
                    product_engine,
                    "__file__",
                    "Unknown",
                )
            )
        )


    if product_ui is not None:

        st.write(
            "product_ui.py:"
        )

        st.code(
            str(
                getattr(
                    product_ui,
                    "__file__",
                    "Unknown",
                )
            )
        )


    if product_management_ui is not None:

        st.write(
            "product_management_ui.py:"
        )

        st.code(
            str(
                getattr(
                    product_management_ui,
                    "__file__",
                    "Unknown",
                )
            )
        )
