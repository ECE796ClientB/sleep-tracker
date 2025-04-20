import { Typography, Box, Button } from "@mui/material";
import { useLocation, useNavigate } from "react-router-dom";
import { sleepGoal } from "../constants/sleepGoals";
import { evaluateSleepInsights } from "../utils/sleepInsights";
import HoursOfSleepChart from "../components/Charts/HoursOfSleepChart";
import HeartRateChart from "../components/Charts/HeartRateChart";
import Recommendations from "../components/Charts/Recommendations";
import { SleepDataPoint } from "../data/sleepData";

interface LocationState {
  username?: string;
}

function Dashboard() {
  const location = useLocation();
  const navigate = useNavigate();
  const { username } = (location.state as LocationState) || {};

  const mockSleepData: SleepDataPoint[] = [
    {
      day: "Monday",
      hours: 7,
      heartRate: 62,
      caffeine: 0,
      exercise: 1,
      stress: "Low",
      age: 30,
    },
    {
      day: "Tuesday",
      hours: 6.5,
      heartRate: 68,
      caffeine: 1,
      exercise: 0.5,
      stress: "Moderate",
      age: 30,
    },
    {
      day: "Wednesday",
      hours: 8,
      heartRate: 65,
      caffeine: 0,
      exercise: 1.5,
      stress: "Low",
      age: 30,
    },
    {
      day: "Thursday",
      hours: 5.5,
      heartRate: 75,
      caffeine: 2,
      exercise: 0,
      stress: "High",
      age: 30,
    },
    {
      day: "Friday",
      hours: 7.8,
      heartRate: 60,
      caffeine: 0.5,
      exercise: 1,
      stress: "Moderate",
      age: 30,
    },
    {
      day: "Saturday",
      hours: 9,
      heartRate: 58,
      caffeine: 0,
      exercise: 2,
      stress: "Low",
      age: 30,
    },
    {
      day: "Sunday",
      hours: 7.2,
      heartRate: 63,
      caffeine: 0,
      exercise: 0.8,
      stress: "Low",
      age: 30,
    },
  ];

  const insights = evaluateSleepInsights(mockSleepData, sleepGoal);

  const handleButtonClick = () => {
    navigate("/dailyinput");
  };

  return (
    <Box className="container">
      <Box sx={{ position: "absolute", top: 16, right: 16 }}>
        <Button
          variant="contained"
          color="primary"
          onClick={handleButtonClick}
        >
          Import Daily Values
        </Button>
      </Box>

      <Typography variant="h4" gutterBottom className="chartTitle">
        Sleep Dashboard
      </Typography>

      {username && (
        <Typography variant="h6" gutterBottom>
          Welcome, {username}!
        </Typography>
      )}

      <Box className="chartContainer">
        <Typography variant="h5" gutterBottom className="chartTitle">
          Hours of Sleep
        </Typography>
        <HoursOfSleepChart data={mockSleepData} />
      </Box>

      <Box className="chartContainer">
        <Typography variant="h5" gutterBottom className="chartTitle">
          Heart Rate
        </Typography>
        <HeartRateChart data={mockSleepData} />
      </Box>

      <Box className="chartContainer">
        <Recommendations insights={insights} />
      </Box>
    </Box>
  );
}

export default Dashboard;
