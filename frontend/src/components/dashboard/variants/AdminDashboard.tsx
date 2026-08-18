
import { getServerSession, Session } from "next-auth";
import { authOptions } from "@/src/lib/authOptions";
import { getDashboard } from "@/src/services/dashboardService";
import { getUsers } from "@/src/services/userService";
import { getAllInventory, getTotalProductsStock } from "@/src/services/inventoryService";
import { getProducts } from "@/src/services/productsService";
import AllProducts from "../Tabs/AllProducts";
import ProductStockView from "../Tabs/ProductStock";
import Users from "../Users";
import RequestsView from "../RequestsView";
import { getAllRequests } from "@/src/services/requestService";
import DataCard from "../DataCard";
import InventoryView from "../InventoryView";


interface Props {
  session: Session
}

async function AdminDashboard({session}:Props) {

    // const session = await getServerSession(authOptions);

    if (!session?.user?.accessToken) {
        throw new Error("Unauthorized");
    }

    const dashboard = await getDashboard(session.user.accessToken);


    // todo: revisit this later
    // const inventory = await getInventory(session.user.accessToken);

    const users = await getUsers(session.user.accessToken);
    const inventory = await getAllInventory(session.user.accessToken);

    const products = await getProducts(session.user.accessToken);

    const productStock = await getTotalProductsStock(
      session.user.accessToken,
      products[0].id
    )

    const requests = await getAllRequests(session.user.accessToken);

    // todo: api calls for per area stuff?
    // ? inventory history?


  return (
    <main className='h-full flex flex-col flex-1 p-4 gap-2'>

      <div className='grid 
      grid-cols-3 gap-2 flex-1 min-h-0
      '>

        <div className="grid grid-cols-3 col-span-3 gap-2">
          <DataCard data={dashboard.totalUsers} label="Users"></DataCard>
          <DataCard data={dashboard.totalProducts} label="Products"></DataCard>
          <DataCard data={dashboard.pendingRequests} label="Pending Requests"></DataCard>
        </div>

        <div className='ring ring-gray-400 p-4 h-full overflow-y-auto min-h-0'>
            <Users users={users}/>          
        </div>

         <div className="flex flex-col ring ring-gray-400 p-4 h-full overflow-y-auto min-h-0">
          <div>
            <h1 className="text-lg font-semibold">Products</h1>
            <AllProducts products={products}/>
          </div>

          <div>
            <h1 className="text-lg font-semibold">Product Stock</h1>
            <ProductStockView stock={productStock} products={products} accessToken={session.user.accessToken}/>
          </div>

        </div>

        <div className='ring ring-gray-400 p-4 h-full overflow-y-auto min-h-0'>
          <RequestsView requests={requests}/>
        </div>

        {/* <div>
          <InventoryView inventory={inventory}/>
        </div> */}

      </div>


        {/* <div>
            <Users users={users}/>          
        </div>
        
        <div>
          <RequestsView requests={requests}/>
        </div> */}

       

        <div>
        </div>

    </main>
  )
}

export default AdminDashboard
