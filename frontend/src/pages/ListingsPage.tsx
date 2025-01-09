import axios from "axios";
import { useEffect, useState } from "react";
import FilterForm from "../components/FilterForm";
import ListingCard from "../components/ListingCard";
import { Listing, Location } from "../types";

function ListingsPage() {
    const [listings, setListings] = useState<Listing[]>([]);
    const [locations, setLocations] = useState<Location[]>([]);

    const [sortBy, setSortBy] = useState<string>("newest");
    const [maxPrice, setMaxPrice] = useState<number>(0);
    const [minPrice, setMinPrice] = useState<number>(0);
    const [locationFilters, setLocationFilters] = useState<Location[]>([]);
    const [keywords, setKeywords] = useState<string[]>([]);

    useEffect(() => {
        fetchListings();
        fetchLocations();
    }, []);

    useEffect(() => {
        fetchListings();
    }, [sortBy]);

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

    const fetchLocations = async () => {
        try {
            const url = "http://127.0.0.1:8000/locations";
            const response = await axios.get(url);
            setLocations(response.data);
        } catch (error) {
            console.error("Error fetching locations: ", error);
        }
    };

    const formatUrlParams = () => {
        const params = new URLSearchParams();

        if (sortBy) {
            params.append("sortBy", sortBy);
        }

        if (maxPrice) {
            params.append("maxPrice", maxPrice.toString());
        }

        if (minPrice) {
            params.append("minPrice", minPrice.toString());
        }

        if (locationFilters.length > 0) {
            locationFilters.forEach((loc) => {
                if (loc.locationType === "city") {
                    params.append("city", loc.name);
                } else {
                    // starts with "region_"
                    params.append("region", loc.name);
                }
            });
        }

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
            <div className="flex flex-row gap-4 p-4 items-start justify-center">
                <div className="max-w-[330px] w-full">
                    <FilterForm
                        sortBy={sortBy}
                        setSortBy={setSortBy}
                        maxPrice={maxPrice}
                        setMaxPrice={setMaxPrice}
                        minPrice={minPrice}
                        setMinPrice={setMinPrice}
                        locations={locations}
                        locationFilters={locationFilters}
                        setLocationFilters={setLocationFilters}
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
