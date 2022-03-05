/*
* This source file is part of an OSTIS project. For the latest info, see http://ostis.net
* Distributed under the MIT License
* (See accompanying file COPYING.MIT or copy at http://opensource.org/licenses/MIT)
*/
#include "HardwareStoresModule.hpp"

SC_IMPLEMENT_MODULE(HardwareStoresModule)

sc_result HardwareStoresModule::InitializeImpl()
{
  m_HardwareStoresService.reset(new HardwareStoresPythonService("HardwareStoresModule/HardwareStoresModule.py"));
  m_HardwareStoresService->Run();
  return SC_RESULT_OK;
}

sc_result HardwareStoresModule::ShutdownImpl()
{
  m_HardwareStoresService->Stop();
  m_HardwareStoresService.reset();
  return SC_RESULT_OK;
}
