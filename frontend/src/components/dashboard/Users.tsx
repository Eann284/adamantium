import React from "react";
import type { User } from "@/src/types/user";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface Props {
  users: User[];
}

function Users({ users }: Props) {
  return (
    <section>
      <input
        type="text"
        placeholder="search"
        className="px-2 w-full ring ring-gray-400 rounded-lg"
      />

      <Table>
        <TableCaption>Users</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[100px]">Name</TableHead>
            <TableHead>Email</TableHead>
            {/* <TableHead>Area</TableHead> */}
            {/* <TableHead className="text-right">Amount</TableHead> */}
          </TableRow>
        </TableHeader>
        <TableBody>
          {users.map((user) => (
            <TableRow key={user.id}>
              <TableCell className="font-medium">{user.name}</TableCell>
              <TableCell>{user.email}</TableCell>
              {/* <TableCell>{user.area}</TableCell> */}
              {/* <TableCell className="text-right">$250.00</TableCell> */}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </section>
  );
}

export default Users;
