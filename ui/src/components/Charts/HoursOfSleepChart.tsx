import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { SleepDataPoint } from "../../data/sleepData";

interface HoursOfSleepChartProps {
  data: SleepDataPoint[];
}

function HoursOfSleepChart({ data }: HoursOfSleepChartProps) {
  return (
    <BarChart
      width={700}
      height={300}
      data={data}
      margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
    >
      <CartesianGrid strokeDasharray="3 3" stroke="#444444" />
      <XAxis dataKey="day" stroke="#ffffff" />
      <YAxis stroke="#ffffff" />
      <Tooltip contentStyle={{ color: "black" }} />
      <Legend />
      <Bar dataKey="hours" fill="#8884d8" />
    </BarChart>
  );
}

export default HoursOfSleepChart;
