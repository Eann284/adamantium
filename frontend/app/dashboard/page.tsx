import { getDashboard } from "@/src/services/dashboardService"
import { getInventory } from "@/src/services/inventoryService";
import { getUsers } from "@/src/services/userService";
import { getServerSession } from "next-auth";
import { authOptions } from "@/src/lib/authOptions";


async function page() {

    const session = await getServerSession(authOptions);

    if (!session?.user?.accessToken) {
        throw new Error("Unauthorized");
    }

    const dashboard = await getDashboard(session.user.accessToken);

    // todo: revisit this later
    // const inventory = await getInventory(session.user.accessToken);

    // const users = await getUsers(session.user.accessToken);


  return (
    <main>
      <h1>Admin Dash</h1>

      <h1>Stats</h1>
      <div>{dashboard.totalUsers} Users</div>
      <div>{dashboard.totalProducts} Products</div>
      <div>{dashboard.pendingRequests} Pending Requests</div>

        <div>
            
        </div>

    </main>
  )
}

export default page
