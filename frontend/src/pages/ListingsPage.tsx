import axios from "axios";
import { useEffect, useState } from "react";
import FilterForm from "../components/FilterForm";
import ListingCard from "../components/ListingCard";
import { SearchResultControls } from "../components/SearchResultControls";
import { Listing, Location, SortBy } from "../types";

function ListingsPage() {
    const [listings, setListings] = useState<Listing[]>([]);
    const [locations, setLocations] = useState<Location[]>([]);

    const [sortBy, setSortBy] = useState<SortBy>("newest");

    const [maxPrice, setMaxPrice] = useState<number>(0);
    const [minPrice, setMinPrice] = useState<number>(0);
    const [locationFilters, setLocationFilters] = useState<Location[]>([]);
    const [size, setSize] = useState<number>(55.0);
    const [showAllSizes, setShowAllSizes] = useState<boolean>(true);
    const [sizeFlexibility, setSizeFlexibility] = useState<boolean>(true);
    const [keywords, setKeywords] = useState<string[]>([]);
    const [bikeTypes, setBikeTypes] = useState<string[]>(["road"]);

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
            params.append("sort_by", sortBy);
        }

        if (maxPrice) {
            params.append("max_price", maxPrice.toString());
        }

        if (minPrice) {
            params.append("min_price", minPrice.toString());
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

        if (!showAllSizes) {
            params.append("size", size.toString());
            if (sizeFlexibility) {
                params.append("size_flexibility", "true");
            }
        }

        // if (keywords.length > 0) {
        //     keywords.forEach((keyword) => {
        //         params.append("keywords", keyword);
        //     });
        // }

        return params.toString();
    };

    return (
        <>
            <div className="flex flex-col gap-4 p-4 items-start justify-center max-w-[940px] mx-auto">
                <FilterForm
                    maxPrice={maxPrice}
                    setMaxPrice={setMaxPrice}
                    minPrice={minPrice}
                    setMinPrice={setMinPrice}
                    locations={locations}
                    locationFilters={locationFilters}
                    setLocationFilters={setLocationFilters}
                    size={size}
                    setSize={setSize}
                    showAllSizes={showAllSizes}
                    setShowAllSizes={setShowAllSizes}
                    sizeFlexibility={sizeFlexibility}
                    setSizeFlexibility={setSizeFlexibility}
                    updateFilters={fetchListings}
                    keywords={keywords}
                    setKeywords={setKeywords}
                    bikeTypes={bikeTypes}
                    setBikeTypes={setBikeTypes}
                />

                <SearchResultControls
                    setSortBy={setSortBy}
                    sortBy={sortBy}
                    numberOfResults={listings.length}
                />
                <div className="grid grid-cols-[repeat(3,1fr)] gap-4 w-full">
                    {listings.map((listing) => (
                        <ListingCard key={listing.id} listing={listing} />
                    ))}
                </div>
            </div>
        </>
    );
}

export default ListingsPage;
