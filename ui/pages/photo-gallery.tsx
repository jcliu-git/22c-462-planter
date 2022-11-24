import {
  Box,
  CustomTheme,
  Grid,
  useTheme,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from "@mui/material";
import { range } from "lodash";
import Image from "next/image";
import React from "react";
import { ExpandMore } from "@mui/icons-material";

interface PhotoDetails {
  img: string;
  title: string;
}

export function ResponsivePhotos({ photos }: { photos: PhotoDetails[] }) {
  const theme = useTheme<CustomTheme>();

  return (
    <Grid
      container
      spacing={2}
      alignItems="center"
      justifyContent="center"
      height="100%"
      sx={{ padding: theme.spacing(3) }}
    >
      {photos.map((photo, index) => (
        <Grid item key={index} flexGrow={1}>
          <Box
            sx={{
              background: theme.palette.background.paper,
              borderRadius: theme.shape.borderRadius,
              padding: theme.spacing(3),
              position: "relative",
            }}
          >
            <Image
              src={`${photo.img}?w=162&auto=format`}
              alt={photo.title}
              loading="lazy"
              width={720}
              height={480}
              style={{
                display: "block",
                width: "100%",
                height: "auto",
              }}
            />
          </Box>
        </Grid>
      ))}
    </Grid>
  );
}

export function TimelapsedPhotos({
  photos,
  interval,
}: {
  photos: PhotoDetails[];
  interval: number;
}) {
  const theme = useTheme<CustomTheme>();

  const [photoIndex, setPhotoIndex] = React.useState(0);

  React.useEffect(() => {
    setTimeout(() => {
      setPhotoIndex((photoIndex + 1) % photos.length);
    }, interval);
  }, [photoIndex, photos, interval]);

  return (
    <Grid
      container
      spacing={2}
      alignItems="center"
      justifyContent="center"
      height="100%"
      sx={{ padding: theme.spacing(3) }}
    >
      <Grid item xs={12}>
        <Box
          sx={{
            background: theme.palette.background.paper,
            borderRadius: theme.shape.borderRadius,
            padding: theme.spacing(3),
            position: "relative",
          }}
        >
          <Image
            src={`${photos[photoIndex].img}?w=162&auto=format`}
            alt={photos[photoIndex].title}
            loading="lazy"
            width={720}
            height={480}
            style={{
              display: "block",
              width: "100%",
              height: "auto",
            }}
          />
        </Box>
      </Grid>
    </Grid>
  );
}

export default function PhotosPage() {
  let photoData: PhotoDetails[] = range(20).map((i) => ({
    img: `https://source.unsplash.com/random/720x480?sig=${i}`,
    title: `Image ${i}`,
  }));
  const [timeLapseEnabled, setTimeLapseEnabled] = React.useState(false);

  const theme = useTheme<CustomTheme>();

  return (
    <Box
      sx={{
        padding: theme.spacing(3),
      }}
    >
      <Accordion onChange={(event, expanded) => setTimeLapseEnabled(expanded)}>
        <AccordionSummary
          expandIcon={<ExpandMore />}
          aria-controls="panel1-content"
          id="panel1-header"
        >
          Time Lapse
        </AccordionSummary>
        <AccordionDetails>
          <TimelapsedPhotos photos={photoData} interval={500} />
        </AccordionDetails>
      </Accordion>
      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMore />}
          aria-controls="panel2-content"
          id="panel2-header"
        >
          Visitors
        </AccordionSummary>
        <AccordionDetails>
          <ResponsivePhotos photos={photoData} />
        </AccordionDetails>
      </Accordion>
    </Box>
  );
}
