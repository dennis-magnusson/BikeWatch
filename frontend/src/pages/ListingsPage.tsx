import axios from "axios";
import { useEffect, useState } from "react";
import FilterForm from "../components/FilterForm";
import ListingCard from "../components/ListingCard";
import { PaginationBar } from "../components/PaginationBar";
import { SearchResultControls } from "../components/SearchResultControls";
import { Listing, Location, SortBy } from "../types";

function ListingsPage() {
    const [listings, setListings] = useState<Listing[]>([]);
    const [locations, setLocations] = useState<Location[]>([]);
    const [categories, setCategories] = useState<string[]>([]);

    const [sortBy, setSortBy] = useState<SortBy>("newest");

    const [maxPrice, setMaxPrice] = useState<number>(0);
    const [minPrice, setMinPrice] = useState<number>(0);
    const [locationFilters, setLocationFilters] = useState<Location[]>([]);
    const [size, setSize] = useState<number>(55.0);
    const [showAllSizes, setShowAllSizes] = useState<boolean>(true);
    const [sizeFlexibility, setSizeFlexibility] = useState<boolean>(true);
    const [keywords, setKeywords] = useState<string[]>([]);
    const [selectedCategories, setSelectedCategories] = useState<string[]>([
        "gravel",
    ]);

    const [page, setPage] = useState<number>(1);
    const [totalResults, setTotalResults] = useState<number>(0);

    const resultsPerPage = 30;

    const totalPages = Math.ceil(totalResults / resultsPerPage);
    console.log(
        `page=${page}, totalResults=${totalResults}, totalPages=${totalPages}, resultsPerPage=${resultsPerPage}`
    );

    const BASE_URL = "http://127.0.0.1:8000";

    useEffect(() => {
        fetchListings();
        fetchLocations();
        fetchCategories();
    }, []);

    useEffect(() => {
        fetchListings();
    }, [sortBy, page]);

    const fetchListings = async () => {
        try {
            const url = `${BASE_URL}/listings?${formatUrlParams()}`;
            console.log(url);
            const response = await axios.get(url);
            setTotalResults(response.data.total);
            setListings(response.data.listings);
        } catch (error) {
            console.error("Error fetching listings: ", error);
        }
    };

    const fetchCategories = async () => {
        try {
            const url = `${BASE_URL}/categories`;
            const response = await axios.get(url);
            setCategories(response.data);
        } catch (error) {
            console.error("Error fetching categories: ", error);
        }
    };

    const fetchLocations = async () => {
        try {
            const url = `${BASE_URL}/locations`;
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

        if (selectedCategories.length > 0) {
            selectedCategories.forEach((category) => {
                params.append("category", category);
            });
        }

        params.append("pagination", page.toString());

        return params.toString();
    };

    const handlePageChange = (newPage: number) => {
        if (newPage >= 1 && newPage <= totalPages) {
            setPage(newPage);
        }
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
                    categories={categories}
                    selectedCategories={selectedCategories}
                    setSelectedCategories={setSelectedCategories}
                />

                <SearchResultControls
                    setSortBy={setSortBy}
                    sortBy={sortBy}
                    numberOfResults={totalResults}
                    numberOfPages={totalPages}
                    page={page}
                />
                <div className="grid grid-cols-[repeat(3,1fr)] gap-4 w-full">
                    {listings.map((listing) => (
                        <ListingCard key={listing.id} listing={listing} />
                    ))}
                </div>

                <PaginationBar
                    page={page}
                    totalPages={totalPages}
                    handlePageChange={handlePageChange}
                />
            </div>
        </>
    );
}

export default ListingsPage;
