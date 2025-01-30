import axios from "axios";
import { useEffect, useState } from "react";
import FilterForm from "../components/FilterForm";
import ListingCard from "../components/ListingCard";
import { PaginationBar } from "../components/PaginationBar";
import { SearchResultControls } from "../components/SearchResultControls";
import { SetAlertDialog } from "../components/SetAlertDialog";
import {
    DEFAULT_MAX_PRICE,
    DEFAULT_MIN_PRICE,
    DEFAULT_SHOW_ALL_SIZES,
    DEFAULT_SIZE,
    DEFAULT_SIZE_FLEXIBILITY,
    DEFAULT_SORT_BY,
} from "../constants";
import { Listing, Location, SortBy } from "../types";

function ListingsPage() {
    const [listings, setListings] = useState<Listing[]>([]);
    const [locations, setLocations] = useState<Location[]>([]);
    const [categories, setCategories] = useState<string[]>([]);

    const [sortBy, setSortBy] = useState<SortBy>(DEFAULT_SORT_BY);

    const [maxPrice, setMaxPrice] = useState<number>(DEFAULT_MAX_PRICE);
    const [minPrice, setMinPrice] = useState<number>(DEFAULT_MIN_PRICE);
    const [hasErrorInPriceFilter, setHasErrorInPriceFilter] =
        useState<boolean>(false);
    const [locationFilters, setLocationFilters] = useState<Location[]>([]);
    const [size, setSize] = useState<number>(DEFAULT_SIZE);
    const [showAllSizes, setShowAllSizes] = useState<boolean>(
        DEFAULT_SHOW_ALL_SIZES
    );
    const [sizeFlexibility, setSizeFlexibility] = useState<boolean>(
        DEFAULT_SIZE_FLEXIBILITY
    );
    const [keywords, setKeywords] = useState<string[]>([]);
    const [selectedCategories, setSelectedCategories] = useState<string[]>([]);

    const [resetButtonDisabled, setResetButtonDisabled] =
        useState<boolean>(false);

    const [page, setPage] = useState<number>(1);
    const [totalResults, setTotalResults] = useState<number>(0);
    const resultsPerPage = 30;
    const totalPages = Math.ceil(totalResults / resultsPerPage);

    const BASE_URL = import.meta.env.VITE_API_BASE_URL;

    useEffect(() => {
        fetchListings();
        fetchLocations();
        fetchCategories();
    }, []);

    useEffect(() => {
        fetchListings();
    }, [sortBy, page]);

    useEffect(() => {
        const isFiltersChanged =
            maxPrice !== DEFAULT_MAX_PRICE ||
            minPrice !== DEFAULT_MIN_PRICE ||
            locationFilters.length > 0 ||
            size !== DEFAULT_SIZE ||
            showAllSizes != DEFAULT_SHOW_ALL_SIZES ||
            sizeFlexibility != DEFAULT_SIZE_FLEXIBILITY ||
            keywords.length > 0 ||
            selectedCategories.length > 0 ||
            sortBy !== DEFAULT_SORT_BY;

        setResetButtonDisabled(!isFiltersChanged);
    }, [
        maxPrice,
        minPrice,
        locationFilters,
        size,
        showAllSizes,
        sizeFlexibility,
        keywords,
        selectedCategories,
        sortBy,
    ]);

    const fetchListings = async () => {
        try {
            const url = `${BASE_URL}/listings?${formatUrlParams()}`;
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

        if (maxPrice !== Infinity) {
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

    const resetSearchFilters = () => {
        setMaxPrice(DEFAULT_MAX_PRICE);
        setMinPrice(DEFAULT_MIN_PRICE);
        setLocationFilters([]);
        setSize(DEFAULT_SIZE);
        setShowAllSizes(DEFAULT_SHOW_ALL_SIZES);
        setSizeFlexibility(DEFAULT_SIZE_FLEXIBILITY);
        setKeywords([]);
        setSelectedCategories([]);
        setSortBy(DEFAULT_SORT_BY);
        setPage(1);
        setHasErrorInPriceFilter(false);
        setResetButtonDisabled(true);
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
                    hasError={hasErrorInPriceFilter}
                    setHasError={setHasErrorInPriceFilter}
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
                    resetSearchFilters={resetSearchFilters}
                    resetButtonDisabled={resetButtonDisabled}
                />

                <SetAlertDialog />

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
