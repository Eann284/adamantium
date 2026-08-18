import { getServerSession } from "next-auth";
import { authOptions } from "@/src/lib/authOptions";
import Navbar from "@/src/components/Navbar";

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await getServerSession(authOptions);

  return (
    <div className="h-screen flex flex-col">
      <Navbar session={session} />

      <div className="flex-1 min-h-0">
      {children}
      </div>
    </div>
  );
}