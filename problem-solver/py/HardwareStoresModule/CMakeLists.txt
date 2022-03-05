file(GLOB_RECURSE SOURCES "*.cpp" "*.hpp")

add_library (HardwareStoresModule SHARED ${SOURCES})

target_include_directories(HardwareStoresModule PRIVATE ${SC_MEMORY_SRC})
target_link_libraries(HardwareStoresModule sc-memory)

add_dependencies(HardwareStoresModule sc-memory)

sc_codegen(HardwareStoresModule ${CMAKE_CURRENT_LIST_DIR})
