interface SleepDataPoint {
  day: string;
  hours: number;
  heartRate: number;
  caffeine: number;
  exercise: number;
  stress: "Low" | "Moderate" | "High" | "Extremely Stressed";
  age: number;
}

const sleepData: SleepDataPoint[] = [];

export default sleepData;
export type { SleepDataPoint };
