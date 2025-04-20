import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { SleepDataPoint } from "../../data/sleepData";

interface HeartRateChartProps {
  data: SleepDataPoint[];
}

function HeartRateChart({ data }: HeartRateChartProps) {
  return (
    <LineChart
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
      <Line type="monotone" dataKey="heartRate" stroke="#ff6b6b" />
    </LineChart>
  );
}

export default HeartRateChart;
