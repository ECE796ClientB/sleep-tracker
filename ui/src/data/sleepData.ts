interface SleepDataPoint {
  date: string;
  hours: number;
  heartRate: number;
}

const sleepData: SleepDataPoint[] = [];

export default sleepData;
export type { SleepDataPoint };
