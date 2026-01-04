import './App.css';
import Home from './Home';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; 
import MainWork from './MainWork';


function App() {
  return (
  <Router> 
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/main-work" element={<MainWork />} />
    </Routes>
  </Router> );   
}

export default App;
