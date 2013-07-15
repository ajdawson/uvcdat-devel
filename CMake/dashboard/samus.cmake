## Provide information about this project
cmake_minimum_required(VERSION 2.8.7)

set(CTEST_SITE "samus.lanl.gov")
set(CTEST_BUILD_COMMAND "/usr/bin/make -j16")

## Populate CMakeCache with block of initial data
file(
  # CMake settings
  WRITE "${CTEST_BINARY_DIRECTORY}/CMakeCache.txt" "
  CMAKE_BUILD_TYPE:STRING=${CTEST_BUILD_CONFIGURATION}
  DART_TESTING_TIMEOUT:STRING=1500
  UPDATE_TYPE:STRING=http
  GIT_PROTOCOL:STRING=http://
  ${PLATFORM_SPECIFIC_CACHE_DATA}

  # Hostname specific library paths
  CDAT_BUILD_ESMF_ESMP:BOOL=ON
  CDAT_ANONYMOUS_LOG:BOOL=OFF
  CDAT_BUILD_ESMF_PARALLEL:BOOL=OFF
  CDAT_BUILD_PARAVIEW:BOOL=ON
  CDAT_BUILD_VISIT:BOOL=ON
  CDAT_DOWNLOAD_SAMPLE_DATA:BOOL=ON
")
