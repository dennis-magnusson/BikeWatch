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

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

const fetchListings = async (params: string) => {
    try {
        const url = `${BASE_URL}/listings?${params}`;
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error("Error fetching listings: ", error);
        return { total: 0, listings: [] };
    }
};

const fetchCategories = async () => {
    try {
        const url = `${BASE_URL}/categories`;
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error("Error fetching categories: ", error);
        return [];
    }
};

const fetchLocations = async () => {
    try {
        const url = `${BASE_URL}/locations`;
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error("Error fetching locations: ", error);
        return [];
    }
};

const formatUrlParams = (filters: any) => {
    const params = new URLSearchParams();

    if (filters.sortBy) {
        params.append("sort_by", filters.sortBy);
    }

    if (filters.maxPrice !== Infinity) {
        params.append("max_price", filters.maxPrice.toString());
    }

    if (filters.minPrice) {
        params.append("min_price", filters.minPrice.toString());
    }

    if (filters.locationFilters.length > 0) {
        filters.locationFilters.forEach((loc: Location) => {
            if (loc.locationType === "city") {
                params.append("city", loc.name);
            } else {
                params.append("region", loc.name);
            }
        });
    }

    if (!filters.showAllSizes) {
        params.append("size", filters.size.toString());
        if (filters.sizeFlexibility) {
            params.append("size_flexibility", "true");
        }
    }

    if (filters.selectedCategories.length > 0) {
        filters.selectedCategories.forEach((category: string) => {
            params.append("category", category);
        });
    }

    params.append("pagination", filters.page.toString());

    return params.toString();
};

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

    useEffect(() => {
        const initializeData = async () => {
            setLocations(await fetchLocations());
            setCategories(await fetchCategories());
            updateListings();
        };
        initializeData();
    }, []);

    useEffect(() => {
        updateListings();
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

    const updateListings = async () => {
        const filters = {
            sortBy,
            maxPrice,
            minPrice,
            locationFilters,
            size,
            showAllSizes,
            sizeFlexibility,
            selectedCategories,
            page,
        };
        const params = formatUrlParams(filters);
        const data = await fetchListings(params);
        setTotalResults(data.total);
        setListings(data.listings);
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
                    updateFilters={updateListings}
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
