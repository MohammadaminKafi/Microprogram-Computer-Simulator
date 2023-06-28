import './App.css';
import { Route,BrowserRouter, Routes } from 'react-router-dom';

import FirstPage from './component/FirstPage';
import SecPage from './component/SecPage';
import ThirdPage from './component/ThirdPage';

function App() {
  return (
  <BrowserRouter>
      <Routes>
        <Route index path='/' element={<FirstPage/>}/> 
        <Route path='/sec' element={<SecPage/>}/>
        <Route path='/third' element={<ThirdPage/>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
