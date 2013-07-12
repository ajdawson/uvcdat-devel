set(LAPACK_MAJOR_SRC 3)
set(LAPACK_MINOR_SRC 4)
set(LAPACK_PATCH_SRC 0)

set(LAPACK_URL http://www.netlib.org/lapack)
set(LAPACK_GZ lapack-${LAPACK_MAJOR_SRC}.${LAPACK_MINOR_SRC}.${LAPACK_PATCH_SRC}.tgz)
set(LAPACK_MD5 02d5706ec03ba885fc246e5fa10d8c70)

set (nm LAPACK)
string(TOUPPER ${nm} uc_nm)
set(${uc_nm}_VERSION ${${nm}_MAJOR_SRC}.${${nm}_MINOR_SRC}.${${nm}_PATCH_SRC})
set(LAPACK_SOURCE ${LAPACK_URL}/${LAPACK_GZ})


if(NOT APPLE)
  if(CMAKE_Fortran_COMPILER)
    add_cdat_package(LAPACK "" "" "")
  endif()
endif()
