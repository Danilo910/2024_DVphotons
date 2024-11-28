cmake_minimum_required(VERSION 2.8)

project(Delphes)

# Set compiler flags for C++ and C with Position Independent Code (PIC) and custom flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -DDROP_CGAL")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC")

# Set the runtime path of the libraries by default but allow to switch it off:
option(SET_RPATH "Set runtime path of the ${project} libraries?" ON)
IF(SET_RPATH)
  # Set up the RPATH so executables find the libraries even when installed in non-default location
  SET(CMAKE_MACOSX_RPATH 1)
  SET(CMAKE_SKIP_BUILD_RPATH  FALSE)
  SET(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE) 
  SET(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")

  # Add the automatically determined parts of the RPATH which point to directories outside
  # the build tree to the install RPATH
  SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

  # Set RPATH for installation if it’s not a system directory
  LIST(FIND CMAKE_PLATFORM_IMPLICIT_LINK_DIRECTORIES "${CMAKE_INSTALL_PREFIX}/lib" isSystemDir)
  IF(${isSystemDir} EQUAL -1)
    SET(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")
  ENDIF(${isSystemDir} EQUAL -1)
ENDIF(SET_RPATH)
    
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake")

# Declare ROOT dependency with optional Eve and RGL components
find_package(ROOT REQUIRED COMPONENTS EG Geom Gui GuiHtml GenVector Hist Physics Matrix Graf RIO Tree Gpad MathCore OPTIONAL_COMPONENTS Eve RGL)
include(${ROOT_USE_FILE})

#nos aseguramos de incluir la direccion correcta
#include_directories(${CMAKE_SOURCE_DIR}/modules)

# Declare Pythia8 dependency
find_package(Pythia8)
if(PYTHIA8_FOUND)
  include_directories(${PYTHIA8_INCLUDE_DIRS})
endif()

# Set default installation library directory if not defined
if(NOT DEFINED CMAKE_INSTALL_LIBDIR)
  set(CMAKE_INSTALL_LIBDIR "lib")
endif()

# Function to generate ROOT dictionaries
function(DELPHES_GENERATE_DICTIONARY dictionary)
  if(${ROOT_VERSION} LESS 6.0)
    ROOT_GENERATE_DICTIONARY(${dictionary} ${ARGN})
  else()
    ROOT_GENERATE_DICTIONARY(${dictionary} MODULE ${dictionary} ${ARGN})
  endif()
endfunction()

# Declare position of all other externals needed
set(DelphesExternals_INCLUDE_DIR ${CMAKE_SOURCE_DIR}/external)

# Add subdirectories for various modules and components
add_subdirectory(classes)
add_subdirectory(converters)
# Uncomment the following line if the display module is necessary
# add_subdirectory(display)
add_subdirectory(examples)
add_subdirectory(external)
add_subdirectory(modules)
add_subdirectory(readers)
add_subdirectory(cards)

# Define the Delphes library, explicitly adding IsolationMuon.cc to avoid duplicate symbol errors
add_library(Delphes SHARED
  $<TARGET_OBJECTS:classes> 
  $<TARGET_OBJECTS:modules> # Automatically includes IsolationMuon.cc
  $<TARGET_OBJECTS:ExRootAnalysis>
  $<TARGET_OBJECTS:fastjet>
  $<TARGET_OBJECTS:tcl>
  $<TARGET_OBJECTS:Hector>
  $<TARGET_OBJECTS:PUPPI>
  $<TARGET_OBJECTS:TrackCovariance>
)

# Define the DelphesDisplay library, if needed (comment out to avoid errors if display is not present)
# add_library(DelphesDisplay SHARED
#   $<TARGET_OBJECTS:classes>
#   $<TARGET_OBJECTS:display>
#   $<TARGET_OBJECTS:modules>
#   modules/IsolationMuon.cc  # Explicitly add IsolationMuon.cc
#   $<TARGET_OBJECTS:ExRootAnalysis>
#   $<TARGET_OBJECTS:fastjet>
#   $<TARGET_OBJECTS:tcl>
#   $<TARGET_OBJECTS:Hector>
#   $<TARGET_OBJECTS:PUPPI>
#   $<TARGET_OBJECTS:TrackCovariance>
# )

# Link libraries for Delphes
target_link_libraries(Delphes ${ROOT_LIBRARIES} ${ROOT_COMPONENT_LIBRARIES})
# Link libraries for DelphesDisplay (uncomment if DelphesDisplay is defined)
# target_link_libraries(DelphesDisplay ${ROOT_LIBRARIES} ${ROOT_COMPONENT_LIBRARIES})



# Link Pythia8 if found
if(PYTHIA8_FOUND)
  target_link_libraries(Delphes ${PYTHIA8_LIBRARIES} ${CMAKE_DL_LIBS})
  # Uncomment the following line if DelphesDisplay is defined
  # target_link_libraries(DelphesDisplay ${PYTHIA8_LIBRARIES} ${CMAKE_DL_LIBS})
endif()

# Install Delphes library to the designated lib directory
install(TARGETS Delphes DESTINATION lib)
# Install DelphesDisplay library if it's enabled
# install(TARGETS DelphesDisplay DESTINATION lib)

