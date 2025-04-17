import { useFormContext } from "react-hook-form";
import { Checkbox, FormControlLabel } from "@mui/material";

interface CheckboxFieldProps {
  id: string;
  label: string;
}

const CheckboxField = ({ id, label }: CheckboxFieldProps) => {
  const { register } = useFormContext();

  return (
    <FormControlLabel
      control={<Checkbox {...register(id)} className="checkboxField" />}
      label={label}
      className="checkboxField"
    />
  );
};

export default CheckboxField;
