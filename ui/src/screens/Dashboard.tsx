import { Typography, Box } from "@mui/material";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  BarChart,
  Bar,
} from "recharts";
import { useLocation } from "react-router-dom";

const sleepHoursData = [
  { day: "Monday", hours: 8 },
  { day: "Tuesday", hours: 7.5 },
  { day: "Wednesday", hours: 6 },
  { day: "Thursday", hours: 7 },
  { day: "Friday", hours: 8 },
  { day: "Saturday", hours: 9 },
  { day: "Sunday", hours: 7 },
];

const bedtimeData = [
  { day: "Monday", bedtime: "22:00" },
  { day: "Tuesday", bedtime: "22:30" },
  { day: "Wednesday", bedtime: "23:00" },
  { day: "Thursday", bedtime: "22:45" },
  { day: "Friday", bedtime: "23:30" },
  { day: "Saturday", bedtime: "00:00" },
  { day: "Sunday", bedtime: "22:15" },
];

const wakeupTimeData = [
  { day: "Monday", wakeupTime: "06:30" },
  { day: "Tuesday", wakeupTime: "07:00" },
  { day: "Wednesday", wakeupTime: "06:00" },
  { day: "Thursday", wakeupTime: "06:45" },
  { day: "Friday", wakeupTime: "07:30" },
  { day: "Saturday", wakeupTime: "08:00" },
  { day: "Sunday", wakeupTime: "07:15" },
];

const convertTimeToNumber = (time: string) => {
  const [hours, minutes] = time.split(":").map(Number);
  return hours + minutes / 60;
};

const bedtimeDataConverted = bedtimeData.map((entry) => ({
  ...entry,
  bedtime: convertTimeToNumber(entry.bedtime),
}));

const wakeupTimeDataConverted = wakeupTimeData.map((entry) => ({
  ...entry,
  wakeupTime: convertTimeToNumber(entry.wakeupTime),
}));

function Dashboard() {
  const location = useLocation();
  const { username } = location.state || {};

  return (
    <Box className="container">
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
          Hours of Sleep Per Day
        </Typography>
        <BarChart
          width={700}
          height={300}
          data={sleepHoursData}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#444444" />
          <XAxis dataKey="day" stroke="#ffffff" />
          <YAxis stroke="#ffffff" />
          <Tooltip />
          <Legend />
          <Bar dataKey="hours" fill="#8884d8" />
        </BarChart>
      </Box>

      <Box className="chartContainer">
        <Typography variant="h5" gutterBottom className="chartTitle">
          Bedtime Over the Week
        </Typography>
        <LineChart
          width={700}
          height={300}
          data={bedtimeDataConverted}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#444444" />
          <XAxis dataKey="day" stroke="#ffffff" />
          <YAxis stroke="#ffffff" />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="bedtime" stroke="#82ca9d" />
        </LineChart>
      </Box>

      <Box className="chartContainer">
        <Typography variant="h5" gutterBottom className="chartTitle">
          Wakeup Time Over the Week
        </Typography>
        <LineChart
          width={600}
          height={300}
          data={wakeupTimeDataConverted}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#444444" />
          <XAxis dataKey="day" stroke="#ffffff" />
          <YAxis stroke="#ffffff" />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="wakeupTime" stroke="#8884d8" />
        </LineChart>
      </Box>
    </Box>
  );
}

export default Dashboard;
