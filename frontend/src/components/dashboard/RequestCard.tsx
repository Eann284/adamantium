
import { MaterialRequest } from '@/src/types/materialRequest'
import { Button } from "@/components/ui/button"
import React from 'react'
import {
  Item,
  ItemActions,
  ItemContent,
  ItemDescription,
  ItemTitle,
} from "@/components/ui/item"

interface Props {
    requests: MaterialRequest;
    onView: ()=>void
}

function RequestCard({requests, onView}:Props) {
  return (
    <Item variant="outline">
        <ItemContent>
          <ItemTitle className='font-semibold text-lg'>MRF - {requests.mrf_id}</ItemTitle>
          <ItemDescription>
           {requests.requestor_email}
          </ItemDescription>
        </ItemContent>
        <ItemActions>
          <Button onClick={onView} variant="outline" size="sm" className="bg-blue-400 text-white font-semibold rounded-sm">
            View
          </Button>
        </ItemActions>
      </Item>
  )
}

export default RequestCard
