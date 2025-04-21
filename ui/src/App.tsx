import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Homepage from "./screens/Homepage";
import Form from "./screens/RegisterForm";
import Dashboard from "./screens/Dashboard";
import DailyInputs from "./screens/DailyInputs";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/create-profile" element={<Form />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/dailyinput" element={<DailyInputs />} />
      </Routes>
    </Router>
  );
}

export default App;
