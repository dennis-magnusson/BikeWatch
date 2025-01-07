import axios from "axios";
import { useEffect, useState } from "react";
import FilterForm from "../components/FilterForm";
import ListingCard from "../components/ListingCard";
import { Listing } from "../types";

function ListingsPage() {
    const [listings, setListings] = useState<Listing[]>([]);
    const [sortBy, setSortBy] = useState<string>("price_low-high");
    const [maxPrice, setMaxPrice] = useState<number>(0);
    const [minPrice, setMinPrice] = useState<number>(0);
    const [cityOrLocation, setCityOrLocation] = useState<string[]>([]);
    const [keywords, setKeywords] = useState<string[]>([]);

    useEffect(() => {
        fetchListings();
    }, []);

    const fetchListings = async () => {
        try {
            const url = `http://127.0.0.1:8000/listings?${formatUrlParams()}`;
            console.log(url);
            const response = await axios.get(url);
            setListings(response.data);
        } catch (error) {
            console.error("Error fetching listings: ", error);
        }
    };

    const formatUrlParams = () => {
        const params = new URLSearchParams();

        // if (sortBy) {
        //     params.append("sort", sortBy);
        // }

        if (maxPrice) {
            params.append("maxPrice", maxPrice.toString());
        }

        if (minPrice) {
            params.append("minPrice", minPrice.toString());
        }

        // if (cityOrLocation.length > 0) {
        //     cityOrLocation.forEach((loc) => {
        //         params.append("locations", loc);
        //     });
        // }

        // if (keywords.length > 0) {
        //     keywords.forEach((keyword) => {
        //         params.append("keywords", keyword);
        //     });
        // }

        return params.toString();
    };

    const howManyFoundText = (
        <div className="col-span-3">
            <p className="text-lg">Found {listings.length} listings</p>
        </div>
    );

    return (
        <>
            <div className="max-w-[900px] mx-auto p-4 flex flex-row gap-4">
                <div className="flex flex-col gap-4">
                    <FilterForm
                        sortBy={sortBy}
                        setSortBy={setSortBy}
                        maxPrice={maxPrice}
                        setMaxPrice={setMaxPrice}
                        minPrice={minPrice}
                        setMinPrice={setMinPrice}
                        cityOrLocation={cityOrLocation}
                        setCityOrLocation={setCityOrLocation}
                        keywords={keywords}
                        setKeywords={setKeywords}
                        updateFilters={fetchListings}
                    />
                </div>

                <div className="grid grid-cols-[repeat(3,1fr)] gap-4">
                    {howManyFoundText}
                    {listings.map((listing) => (
                        <ListingCard key={listing.id} listing={listing} />
                    ))}
                </div>
            </div>
        </>
    );
}

export default ListingsPage;
