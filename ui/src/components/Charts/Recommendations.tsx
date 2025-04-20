import { Typography, Box } from "@mui/material";

interface RecommendationsProps {
  insights: string[];
}

function Recommendations({ insights }: RecommendationsProps) {
  return (
    <div>
      <Typography variant="h5" gutterBottom className="chartTitle">
        Recommendations
      </Typography>
      {insights.map((msg, idx) => (
        <Box key={idx} marginBottom={2} paddingLeft={6}>
          <Typography variant="body1">{msg}</Typography>
        </Box>
      ))}
    </div>
  );
}

export default Recommendations;
