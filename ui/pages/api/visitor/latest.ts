import { NextApiRequest, NextApiResponse } from "next";

type response = {
  uri: string;
};

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<response>
) {
  res.status(200).json({
    uri: "https://picsum.photos/200/300",
  });
}
