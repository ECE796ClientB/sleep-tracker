import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Homepage from "./screens/Homepage";
import Form from "./screens/RegisterForm";
import Dashboard from "./screens/Dashboard";
import DailyInputs from "./screens/DailyInputs";
import { FormProvider, useForm } from "react-hook-form";
import { Box } from "@mui/material";

function App() {
  const methods = useForm();
  const { handleSubmit, reset } = methods;

  const onSubmitDailyInputs = (data) => {
    console.log(data);
    reset();
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/create-profile" element={<Form />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route
          path="/dailyinput"
          element={
            <FormProvider {...methods}>
              <Box sx={{ padding: 3 }}>
                <form onSubmit={handleSubmit(onSubmitDailyInputs)}>
                  <DailyInputs />
                </form>
              </Box>
            </FormProvider>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
