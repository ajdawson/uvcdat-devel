set(LIBCF_MAJOR 1)
set(LIBCF_MINOR 0)
set(LIBCF_PATCH beta11)
set(LIBCF_VERSION ${LIBCF_MAJOR}.${LIBCF_MINOR}-${LIBCF_PATCH})
set(LIBCF_URL ${LLNL_URL})
set(LIBCF_GZ libcf-${LIBCF_VERSION}.tar.gz)
set(LIBCF_MD5 aba4896eab79d36c7283fc7b75fb16ee)

add_cdat_package(libcf "" "" "")