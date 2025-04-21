import { SleepDataPoint } from "../data/sleepData";

export function evaluateSleepInsights(
  data: SleepDataPoint[],
  goal: string | null
): string[] {
  const messages: Set<string> = new Set();
  const numDays = data.length;

  if (numDays === 0) {
    return ["Not enough sleep data to generate insights."];
  }

  const age: number = data[0]?.age || 30;
  const avgHeartRate: number =
    data.reduce((sum, d) => sum + d.heartRate, 0) / numDays;
  const avgHours: number =
    data.reduce((sum, d) => sum + d.hours, 0) / numDays;

  const daysWithLowSleep = data.filter((d) => d.hours < 6);
  const daysWithHighCaffeineGt3 = data.filter((d) => d.caffeine > 3);
  const daysWithHighCaffeineGe3 = data.filter((d) => d.caffeine >= 3);
  const daysWithLowCaffeine = data.filter((d) => d.caffeine <= 1);
  const daysWithHighStress = data.filter(
    (d) => d.stress === "High stress" || d.stress === "Extremely Stressed"
  );
  const daysWithLowOrModerateStress = data.filter(
    (d) => d.stress === "No stress" || d.stress === "Low stress" || d.stress === "Moderate stress"
  );
  const daysWithHighHeartRate = data.filter((d) => d.heartRate > 85);
  const daysWithNoExercise = data.filter((d) => d.exercise === 0);
  const daysWithSomeExercise = data.filter((d) => d.exercise >= 0.5);
  const daysWithHighExercise = data.filter((d) => d.exercise > 2);
  const daysWithSufficientSleep = data.filter((d) => d.hours >= 7);
  const daysWithStableHeartRate = data.filter(
    (d) => Math.abs(d.heartRate - avgHeartRate) <= 5
  );

  if (daysWithLowSleep.length >= 3) {
    messages.add(
      "You're not getting as much sleep as you should be. Try setting a consistent bedtime and winding down earlier to recharge fully."
    );
  }
  if (daysWithHighCaffeineGt3.length >= 1) {
    messages.add(
      "Sounds like you might be having too much caffeine, which is preventing you from getting good quality sleep. Try cutting back or switching to decaf after lunch to help your body wind down."
    );
  }
  if (daysWithHighStress.length >= 3) {
    messages.add(
      "You seem to be very stressed the last few days. Try to calm yourself down with some deep breaths or meditation before bed."
    );
  }
  if (avgHeartRate > 85) {
    messages.add(
      "Your average heart rate seems high during sleep. Try to cut back on coffee or alcohol later in the day and try to do something calming (like drinking tea!) before bed."
    );
  }
  if (numDays >= 7 && daysWithNoExercise.length >= 7) {
    messages.add(
      "Your sleep could be better even with a little bit of exercise. Go outside and start out with a brisk 15 minute walk to help your body settle down at night."
    );
  }

  if (goal === "Improving sleep duration") {
    const goalDaysBelow8 = data.filter((d) => d.hours < 8);
    if (goalDaysBelow8.length >= 5) {
      messages.add(
        "You're not hitting your ideal sleep duration just yet. Try moving your bedtime earlier by 15-30 minutes to get more rest."
      );
    }
  } else if (goal === "Improve Sleep Quality") {
    if (daysWithHighHeartRate.length >= 5) {
      messages.add(
        "You're not getting much deep sleep, which your body needs to physically recover. Try limiting screen time and alcohol before bed, and keep your room dark and cool."
      );
    }
  } else if (goal === "Reduce Wakeups") {
    if (daysWithHighCaffeineGt3.length >= 1) {
      messages.add(
        "You may be waking up more often than you'd like. Try limiting fluid intake after 8 PM and reducing bedroom noise with a fan or white noise."
      );
    }
  } else if (goal === "Feel more rested during Day") {
    if (
      avgHours >= 7 &&
      avgHours <= 8 &&
      (daysWithHighStress.length >= 1 ||
        daysWithHighCaffeineGe3.length >= 1)
    ) {
      messages.add(
        "Even with enough sleep, stress and caffeine can reduce how refreshed you feel. Try a calming activity before bed and taper off caffeine earlier in the day."
      );
    }
  }

  if (
    daysWithHighHeartRate.length >= 1 &&
    daysWithHighCaffeineGt3.length >= 1
  ) {
    messages.add(
      "You seem to be restless at night. Try winding down earlier and avoiding intense workouts or stimulants close to bedtime."
    );
  }
  if (
    daysWithHighCaffeineGe3.length >= 1 &&
    daysWithLowSleep.length >= 1
  ) {
    messages.add(
      "Stimulants may be keeping you from falling into restful sleep. Try reducing caffeine, especially after 12 PM."
    );
  }
  if (daysWithNoExercise.length >= 1 && daysWithHighStress.length >= 1) {
    messages.add(
      "Physical activity is one of the best ways to reduce stress and improve sleep. Even a short walk can help your mind and body settle at night."
    );
  }
  if (daysWithHighExercise.length >= 1 && daysWithLowSleep.length >= 1) {
    messages.add(
      "Your body may not be recovering enough from physical strain. Try extending your sleep by 30-60 minutes or shifting workouts earlier."
    );
  }
  if (age > 50 && daysWithHighHeartRate.length >= 1) {
    messages.add(
      "Deep sleep naturally declines with age, but you can support it by limiting light and noise, and avoiding heavy meals before bed."
    );
  }

  if (daysWithSufficientSleep.length >= 5) {
    messages.add(
      "You're hitting a healthy sleep rhythm—amazing work! Keep it up and notice how your energy stays strong during the day."
    );
  }
  if (
    numDays === 7 &&
    daysWithLowOrModerateStress.length === 7 &&
    daysWithSufficientSleep.length === 7
  ) {
    messages.add(
      "Low stress and solid sleep—you're creating the ideal environment for recovery. Keep doing what's working for you!"
    );
  }
  if (daysWithStableHeartRate.length >= 5) {
    messages.add(
      `Your heart rate (${avgHeartRate.toFixed(
        0
      )} bpm avg) is staying steady at night—a great sign that your body is recovering well.`
    );
  }

  if (
    daysWithLowCaffeine.length >= numDays / 2 &&
    daysWithSufficientSleep.length >= numDays / 2 &&
    numDays >= 3
  ) {
    messages.add(
      "You're managing your caffeine intake responsibly—your sleep thanks you!"
    );
  }
  if (daysWithSomeExercise.length >= 3) {
    messages.add(
      "Great movement habits—regular activity like this supports deeper sleep and better recovery."
    );
  }

  if (messages.size === 0) {
    messages.add(
      "Even small changes to your sleep routine—like turning off screens earlier or setting a consistent bedtime—can make a big difference over time."
    );
  }

  return Array.from(messages);
}
