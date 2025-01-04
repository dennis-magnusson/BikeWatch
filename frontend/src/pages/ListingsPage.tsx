import { Card, CardContent, CardHeader } from "@/components/ui/card";
import axios from "axios";
import { useEffect, useState } from "react";
import FilterForm from "../components/FilterForm";
import ListingCard from "../components/ListingCard";
import { Listing } from "../types";

function ListingsPage() {
    const [listings, setListings] = useState<Listing[]>([]);

    useEffect(() => {
        const fetchListings = async () => {
            try {
                const response = await axios.get(
                    `http://127.0.0.1:8000/listings`
                );
                setListings(response.data);
            } catch (error) {
                console.error("Error fetching listings: ", error);
            }
        };

        fetchListings();
    }, []);

    return (
        <>
            <div className="max-w-[900px] mx-auto p-4 flex flex-row gap-4">
                <div>
                    <Card>
                        <CardHeader>
                            <h2 className="font-bold text-3xl">Filter</h2>
                        </CardHeader>
                        <CardContent>
                            <FilterForm />
                        </CardContent>
                    </Card>
                </div>
                <div className="grid grid-cols-[repeat(3,1fr)] gap-4">
                    {listings.map((listing) => (
                        <ListingCard key={listing.id} listing={listing} />
                    ))}
                </div>
            </div>
        </>
    );
}

export default ListingsPage;
