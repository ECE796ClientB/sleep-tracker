interface SleepDataPoint {
  day: string;
  hours: number;
  heartRate: number;
  caffeine: number;
  exercise: number;
  stress: "No stress" | "Low stress" | "Moderate stress" | "High stress" | "Extremely Stressed";
  age: number;
}

const sleepData: SleepDataPoint[] = [];

export default sleepData;
export type { SleepDataPoint };
