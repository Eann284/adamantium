import EditRequest from "@/src/components/dashboard/EditRequest"
import { authOptions } from "@/src/lib/authOptions";
import { getServerSession } from "next-auth";


async function page({params}:{params: Promise<{mrf_id:string}>}) {

    const {mrf_id} = await params;


  return (
    <div>
      <EditRequest mrf_id={mrf_id}/>
    </div>
  )
}

export default page
