import { MaterialRequest } from '@/src/types/materialRequest'
import React from 'react'
import {
  Item,
  ItemActions,
  ItemContent,
  ItemDescription,
  ItemTitle,
} from "@/components/ui/item"
import { Button } from '@/components/ui/button';
interface Props {
    releases: MaterialRequest;
    onView: ()=>void
}

function ReleaseCard({releases, onView}:Props) {
  return (
    
    <Item variant="outline">
        <ItemContent>
          <ItemTitle className='font-semibold text-lg'>MRF - {releases.mrf_id}</ItemTitle>
          <ItemDescription>
           {releases.requestor_email}
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

export default ReleaseCard
