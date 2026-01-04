import logo from './logo.png';
import './App.css';
import './Home.css';
import { useNavigate } from 'react-router-dom';

function Home() {
  const navigate = useNavigate();

  return (
    <div className="App">
      <header className="App-header">
      <h1>Syllabus to Calendar App</h1>
      <h3>Le Talent N'existe pas</h3> 
      <button className='lets-go-btn' onClick={() => navigate('/main-work')}> 
        Let's Go!
      </button>
        <img src={logo} className="App-logo" alt="logo" />
      </header>
    </div>
  );
}
export default Home;
