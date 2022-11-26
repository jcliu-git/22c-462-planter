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
import { useDispatch, useSelector } from "react-redux";
import { IPhotoData, RootState } from "../models/store";

export function VisitorPhotos({ photos }: { photos: IPhotoData[] }) {
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
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <Box
              sx={{
                background: `url(${photo.filepath})`,
                backgroundSize: "contain",
                backgroundPosition: "center",
                backgroundRepeat: "no-repeat",
                height: "70vh",
                width: "100%",
              }}
            ></Box>
            {/* <Image
              src={`${photo.filepath}?w=162&auto=format`}
              alt={photo.filepath}
              loading="lazy"
              width={720}
              height={480}
              style={{
                display: "block",
                width: "100%",
                height: "auto",
              }}
            /> */}
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
  photos: IPhotoData[];
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
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <Box
            sx={{
              background: `url(${photos[photoIndex].filepath})`,
              backgroundSize: "contain",
              backgroundPosition: "center",
              backgroundRepeat: "no-repeat",
              height: "70vh",
              width: "100%",
            }}
          ></Box>
          {/* <Image
            src={`${photos[photoIndex].filepath}?w=162&auto=format`}
            alt={photos[photoIndex].filepath}
            loading="lazy"
            width={720}
            height={480}
            style={{
              display: "block",
              width: "auto",
              height: "100%",
              // height: "auto",
              // maxHeight: "100vh",
            }}
          /> */}
        </Box>
      </Grid>
    </Grid>
  );
}

export default function PhotosPage() {
  const [timeLapseEnabled, setTimeLapseEnabled] = React.useState(false);

  const photos = useSelector((state: RootState) => state.gallery.photos);

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
          {photos.timelapse.length ? (
            <TimelapsedPhotos photos={photos.timelapse} interval={500} />
          ) : null}
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
          {photos.visitors.length ? (
            <VisitorPhotos photos={photos.visitors} />
          ) : null}
        </AccordionDetails>
      </Accordion>
    </Box>
  );
}
