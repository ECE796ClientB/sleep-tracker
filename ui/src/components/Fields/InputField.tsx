import { TextField } from "@mui/material";
import { useFormContext } from "react-hook-form";

interface InputFieldProps {
  id: string;
  label: string;
  type?: string;
  required?: boolean;
}

const InputField = ({
  id,
  label,
  type = "text",
  required = true,
}: InputFieldProps) => {
  const { register } = useFormContext();

  return (
    <TextField
      id={id}
      label={label}
      variant="outlined"
      size="small"
      type={type}
      required={required}
      {...register(id)}
      slotProps={{
        inputLabel: {
          shrink: true,
        },
      }}
      className="textField"
    />
  );
};

export default InputField;
