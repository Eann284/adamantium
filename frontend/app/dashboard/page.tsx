import { getDashboard } from "@/src/services/dashboardService"
import { getAllInventory, getInventory } from "@/src/services/inventoryService";
import { getUsers } from "@/src/services/userService";
import { getServerSession } from "next-auth";
import { authOptions } from "@/src/lib/authOptions";
import { User } from "@/src/types/user";
import Users from "@/src/components/dashboard/Users";
import InventoryView from "@/src/components/dashboard/InventoryView";
import { getAllRequests } from "@/src/services/requestService";
import RequestsView from "@/src/components/dashboard/RequestsView";


async function page() {

    const session = await getServerSession(authOptions);

    if (!session?.user?.accessToken) {
        throw new Error("Unauthorized");
    }

    const dashboard = await getDashboard(session.user.accessToken);


    // todo: revisit this later
    // const inventory = await getInventory(session.user.accessToken);

    const users = await getUsers(session.user.accessToken);
    const inventory = await getAllInventory(session.user.accessToken);
    const requests = await getAllRequests(session.user.accessToken);

    // todo: api calls for per area stuff?
    // ? inventory history?


  return (
    <main className="grid grid-cols-3 p-4">
      <h1 className="col-span-3">Admin Dash</h1>

      <div>{dashboard.totalUsers} Users</div>
      <div>{dashboard.totalProducts} Products</div>
      <div>{dashboard.pendingRequests} Pending Requests</div>

        <div>
            <Users users={users}/>          
        </div>
        <div>
          <InventoryView inventory={inventory}/>
        </div>
        <div>
          <RequestsView requests={requests}/>
        </div>

    </main>
  )
}

export default page
