#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "tumopp::tumopp-exe" for configuration "Release"
set_property(TARGET tumopp::tumopp-exe APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(tumopp::tumopp-exe PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/tumopp"
  )

list(APPEND _cmake_import_check_targets tumopp::tumopp-exe )
list(APPEND _cmake_import_check_files_for_tumopp::tumopp-exe "${_IMPORT_PREFIX}/bin/tumopp" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
