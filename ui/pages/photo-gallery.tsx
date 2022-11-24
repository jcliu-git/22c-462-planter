import { ImageList, ImageListItem } from "@mui/material";
import { range } from "lodash";
import Image from "next/image";

export default function PhotosPage() {
  let itemData = range(20).map((i) => ({
    img: `https://picsum.photos/200/300?random=${i}`,
    title: `Image ${i}`,
  }));

  return (
    <ImageList sx={{ width: 500, height: 450 }} cols={3} rowHeight={164}>
      {itemData.map((item) => (
        <ImageListItem key={item.img}>
          <Image
            width={300}
            height={200}
            src={item.img}
            alt={item.title}
            loading="lazy"
          />
        </ImageListItem>
      ))}
    </ImageList>
  );
}
