import { Button, Stack, Box } from "@mui/material";
import { useForm, SubmitHandler, FormProvider } from "react-hook-form";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AccountDetails from "../components/Form/AccountDetails";
import BasicInfo from "../components/Form/BasicInfo";
import SleepGoals from "../components/Form/SleepGoals";

interface FormData {
  username: string;
  password: string;
  firstName: string;
  lastName: string;
  age: number;
  gender: string;
  height: string;
  weight: string;
  sleep_goals: {
    duration?: boolean;
    quality?: boolean;
    wakeups?: boolean;
    rest?: boolean;
  };
}

function Form() {
  const methods = useForm<FormData>();
  const { handleSubmit, reset } = methods;
  const [patientId, setPatientId] = useState("");
  const navigate = useNavigate();

  const onSubmit: SubmitHandler<FormData> = async (data) => {
    
    // Send POST request to backend
    const payload =
    {
      username: data.username,
      password: data.password,
      firstName: "Joe",
      lastName: "Balsamo",
      age: data.age,
      gender: data.gender,
      height: data.height,
      weight: data.weight,
      sleepGoals: "Goals"
    };
  
    try
    {
      const response = await fetch('https://sleep-tracker-backend.up.railway.app/createPatient', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Tells the backend to expect JSON
        },
        body: JSON.stringify(payload),
      });
      
      const responseData = await response.json();
      if(responseData.patientId != 0) 
        {
          setPatientId(data.patientId);
  
           // Redirect to dashboard page and pass the Patient ID
          console.log("Successfully Created Patient: " + patientId);
          navigate("/dashboard", { state: { patientId } });
        }
        else
        {
          console.log("Could not create patient");
        }
    }
    catch (err)
    {
      console.error('Error:', err);
    }

    reset();
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      sx={{
        width: "500px",
        maxWidth: "90%",
        height: "auto",
        margin: "auto",
        padding: "20px",
      }}
    >
      <FormProvider {...methods}>
        <form onSubmit={handleSubmit(onSubmit)}>
          <Stack spacing={2}>
            <AccountDetails />
            <BasicInfo />
            <SleepGoals />
            <Button type="submit" variant="contained">
              Submit
            </Button>
          </Stack>
        </form>
      </FormProvider>
    </Box>
  );
}

export default Form;
