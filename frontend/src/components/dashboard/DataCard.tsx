import React from "react";

import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface Props {
  data: number;
  label: string;
}

function DataCard({ data, label }: Props) {
  return (
    // <div className='p-4 bg-blue-500 text-xl text-white font-semibold rounded-sm'>
    //   {data} {label}
    // </div>

    <Card className="ring-2 ring-blue-500">
      <CardHeader>
        <CardTitle>
          <h1 className="text-xl text-blue-500 font-semibold">{data} {label}</h1>
        </CardTitle>
      </CardHeader>
     

    </Card>
  );
}

export default DataCard;
