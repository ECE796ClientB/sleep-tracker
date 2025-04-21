import {
  Box,
  Typography,
  Button,
  Stack,
  RadioGroup,
  FormControlLabel,
  Radio,
  FormControl,
} from "@mui/material";
import { useState } from "react";
import InputField from "../components/Fields/InputField";
import { useLocation, useNavigate } from "react-router-dom";
import { useForm, FormProvider, SubmitHandler } from "react-hook-form";

interface FormData {
  caffeine: number;
  exercise: number;
  stressLevel: string;
}

function DailyInputs() {
  const form = useForm<FormData>();
  const navigate = useNavigate();
  const location = useLocation();
  const patientId = location.state?.patientId;
  const { handleSubmit } = form;
  const [stressLevel, setStressLevel] = useState("0");

  const stressLabels = {
    0: "No stress",
    1: "Low stress",
    2: "Moderate stress",
    3: "High stress",
    4: "Extremely stressed",
  };

  const handleStressChange = (event) => {
    setStressLevel(event.target.value);
    form.setValue("stressLevel", event.target.value);
  };

  const onSubmit: SubmitHandler<FormData> = async (data) => {
    const stressLevelString = stressLabels[data.stressLevel];
    console.log("Submitted");
    // Send POST request to backend
    const payload = {
      patientId: patientId,
      caffeine: Number(data.caffeine),
      exercise: Number(data.exercise),
      stressLevel: stressLevelString,
    };

    try {
      const response = await fetch(
        `https://sleep-tracker-backend.up.railway.app/logDailies?patientId=${patientId}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        }
      );

      const text = await response.text();
      console.log("Raw response:", text);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status} - ${text}`);
      }
      const responseData = JSON.parse(text);
      console.log("Sent");
      navigate("/dashboard", { state: { patientId: patientId } });
    } catch (err) {
      console.error("Error:", err);
    }
  };

  return (
    <Box sx={{ maxWidth: 600, mx: "auto", padding: 3 }}>
      <Typography variant="h3" gutterBottom>
        Daily Values
      </Typography>
      <FormProvider {...form}>
        <form onSubmit={handleSubmit(onSubmit)}>
          <Stack spacing={3}>
            <InputField
              id="caffeine"
              label="Caffeine Intake (cups of coffee)"
              type="number"
            />
            <InputField
              id="exercise"
              label="Exercise (hours spent today)"
              type="number"
            />

            <Typography variant="h6">Stress Level:</Typography>
            <FormControl component="fieldset">
              <RadioGroup
                aria-label="stress-level"
                name="stressLevel"
                value={stressLevel}
                onChange={handleStressChange}
              >
                {Object.entries(stressLabels).map(([value, label]) => (
                  <FormControlLabel
                    key={value}
                    value={value}
                    control={<Radio />}
                    label={label}
                  />
                ))}
              </RadioGroup>
            </FormControl>
            <Button
              variant="contained"
              color="primary"
              type="submit"
              sx={{ marginTop: 3 }}
            >
              Submit Daily Values
            </Button>
          </Stack>
        </form>
      </FormProvider>
    </Box>
  );
}

export default DailyInputs;
