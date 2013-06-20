# create an external project to install pyzmq,
# and configure and build it

include(@cdat_CMAKE_BINARY_DIR@/cdat_common_environment.cmake)

if (INTERNET_ACCESS STREQUAL "ON") 
    set(EGG_GZ )
else ()
    set(EGG_GZ ${CDAT_PACKAGE_CACHE_DIR}/${PYZMQ_GZ})
endif()

ExternalProject_Add(pyzmq
  DOWNLOAD_COMMAND ""
  WORKING_DIRECTORY ${CMAKE_INSTALL_PREFIX}
  BUILD_IN_SOURCE 1
  CONFIGURE_COMMAND ""
  BUILD_COMMAND ""
  INSTALL_COMMAND ${EGG_CMD} pyzmq==${PYZMQ_VERSION} ${EGG_GZ}
  DEPENDS ${pyzmq_deps}
  ${ep_log_options}
  )
