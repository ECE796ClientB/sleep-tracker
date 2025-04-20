import { Typography, Box, Button } from "@mui/material";
import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from "react-router-dom";
import { sleepGoal } from "../constants/sleepGoals";
import { evaluateSleepInsights } from "../utils/sleepInsights";
import HoursOfSleepChart from "../components/Charts/HoursOfSleepChart";
import HeartRateChart from "../components/Charts/HeartRateChart";
import Recommendations from "../components/Charts/Recommendations";
import { SleepDataPoint } from "../data/sleepData";


function Dashboard() {
  const location = useLocation();
  const navigate = useNavigate();
  const patientId = location.state?.patientId;
  const [sleepData, setSleepData] = useState<SleepDataPoint[]>([]);

  const mockSleepData: SleepDataPoint[] = [
    {
      date: "Monday",
      hours: 7,
      heartRate: 62,
    },
    {
      date: "Tuesday",
      hours: 6.5,
      heartRate: 68,
    },
    {
      date: "Wednesday",
      hours: 8,
      heartRate: 65,
    },
    {
      date: "Thursday",
      hours: 5.5,
      heartRate: 75,
    },
    {
      date: "Friday",
      hours: 7.8,
      heartRate: 60,
    },
    {
      date: "Saturday",
      hours: 9,
      heartRate: 58,
    },
    {
      date: "Sunday",
      hours: 7.2,
      heartRate: 63,
    },
  ];

  // Get Sleep Data
  useEffect(() => {

    // Create GET request params
    const params = new URLSearchParams(
      {
        patientId: patientId
      }
    );

    // This runs once when the component mounts
    const fetchData = async () => {
      try 
      {
        const response = await fetch(`https://sleep-tracker-backend.up.railway.app/sleepData?${params}`);
        const result = await response.json();

        // Create the Sleep Data
        const sleepDataPoints: SleepDataPoint[] = result.map(item => ({
          date: item.day,
          hours: item.hours,
          heartRate: item.heartRate,
        }));

        setSleepData(sleepDataPoints)
      } 
      catch (error)
      {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const insights = evaluateSleepInsights(sleepData, sleepGoal);

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

      <Box className="chartContainer">
        <Typography variant="h5" gutterBottom className="chartTitle">
          Hours of Sleep
        </Typography>
        <HoursOfSleepChart data={sleepData} />
      </Box>

      <Box className="chartContainer">
        <Typography variant="h5" gutterBottom className="chartTitle">
          Heart Rate
        </Typography>
        <HeartRateChart data={sleepData} />
      </Box>

      <Box className="chartContainer">
        <Recommendations insights={insights} />
      </Box>
    </Box>
  );
}

export default Dashboard;
