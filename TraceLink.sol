// SPDX-License_Identifier: MIT (open-source)
pragma solidity ^0.6.0;               // Solidity Version
pragma experimental ABIEncoderV2;     // Library for calculations

// Contract that defines all data structures & functions
contract TraceLink {
    // State variables
    mapping(uint => Product) public Pmap;   // Mapping for products
    uint public PmapSize = 0;               // Size of above mapping
    mapping(uint => Company) public Cmap;   // Mapping for companies
    uint public CmapSize = 0;               // Size of above mapping

    // Global variables used for functions
    uint current_pid;
    uint current_fcid;
    uint current_tcid;

    // Product structure with attributes
    struct Product {
        uint PId;
        string PName;
        uint Brand;
        string Desc;
        int[] clicks;          // Will be size of quantity, initialized to 0s
        SCSection[] SChain;    // Will contain logs
    }

    // Company structure will attributes
    struct Company {
        uint CId;
        string CName;
        string CType;
        uint[] CProducts;
    }

    // Log structure will attributes
    struct SCSection {
        uint ProductId;
        uint FromId;
        uint ToId;
        string EmpId;
        bool comp;     //Used for internal logic
        string Task;
        string Location;
        uint TimeOfHandOver;
    }

    //Function or TRANSACTION that updates the product array
    //Company Id here will be picked up during login time
    //Timestamps & location will be taken automatically in backend
    function StoreProduct(
        uint CompanyId,
        string memory ProductName,
        string memory pdesc,
        uint quant,
        uint FId,
        uint To_Id,
        string memory EmployeeId,
        bool comp,
        string memory TaskDetails,
        string memory Current_Location
    ) public returns (uint ProductId) {
        ProductId = PmapSize + 1;
        Product storage p = Pmap[ProductId];    // Declaring product
        p.PId = ProductId;                      // Assigning values
        p.PName = ProductName;
        p.Brand = CompanyId;
        p.Desc = pdesc;
        for (uint256 i = 0; i < quant; i++) {   // Adding 0s, quant times
            p.clicks.push(0);
        }
        p.SChain.push(        // Adding first log
            SCSection(
                PmapSize + 1,
                FId,
                To_Id,
                EmployeeId,
                comp,
                TaskDetails,
                Current_Location,
                block.timestamp
            )
        );
        PmapSize += 1;
        Cmap[CompanyId].CProducts.push(ProductId);
        return ProductId;
    }

    // Function to get company names from company IDs
    function showC()
        public
        view
        returns (string memory fc, string memory tc)
    {
        fc = Cmap[current_fcid].CName;
        tc = Cmap[current_tcid].CName;
        return (fc, tc);
    }

    // Function that assigns IDs to global variables to be used by showC()
    function updateCft(uint fcid, uint tcid) public {
        current_fcid = fcid;
        current_tcid = tcid;
    }

    // Function that returns assigned product ID
    function showPDetails() public view returns (Product memory p) {
        p = Pmap[current_pid];
        return p;
    }

    // Function to update count of product piece
    function updateCount(uint pid, uint piece_num) public {
        Product storage p = Pmap[pid];
        p.clicks[piece_num - 1] += 1;
        current_pid = pid;
    }

    // Function that adds log to product
    function StoreSCS(
        uint Product_Id,
        uint FId,
        uint To_Id,
        string memory EmployeeId,
        bool comp,
        string memory TaskDetails,
        string memory Current_Location
    ) public {
        SCSection[] memory chain = Pmap[Product_Id].SChain;
        uint lastC = chain[chain.length - 1].ToId;
        
        if ((lastC == FId)      // Checks if user is allowed to add log
        || (lastC == FId)) {
            Pmap[Product_Id].SChain.push(
                SCSection(
                    Product_Id,
                    FId,
                    To_Id,
                    EmployeeId,
                    comp,
                    TaskDetails,
                    Current_Location,
                    block.timestamp
                )
            );
        }
    }

    // Function to add company, internally used
    function addCompany(
        string memory Name,
        string memory CompanyType
    ) public  {
        Company storage c = Cmap[CmapSize+1];
        c.CId = CmapSize+1;
        c.CName = Name;
        c.CType = CompanyType;
        CmapSize += 1;
    }

    // Function to show mappping sizes
    function showCP()
        public
        view
        returns (uint csize, uint psize)
    {
        csize = CmapSize;
        psize = PmapSize;
        return (csize, psize);
    }

    // Executes upon contract creation & contains initial data
    constructor() public {
        addCompany("Gucci", "Luxury Fashion");
        addCompany("Globalx", "Logistics");
        addCompany("Barari", "Olive Oil Manufacturing");
        addCompany("Madina", "Hypermarket Francise");
        addCompany("Offer House Ent.", "We buy bulk from manufacturers & sell at our retail stores");
        addCompany("XiaXiozhi", "Cheap tech contractors");
        addCompany("Factory Express", "Contract factory");
        addCompany("AliBaba", "Large E-commerce store");
        StoreProduct(
            1, "GG Marmount Small Shoulder Bag", '2023 Winter Collection', 50, 1, 1, 
            "m00 851749", //Automatically taken
            true, "Order given to our factory 112 in Ajman", "Al Sufouh, Dubai"  //Automatically taken
        );
        StoreSCS(1, 1, 1, 'm00375638', true, 'Manufactured products handed over to our warehouse 065',
                'Sreet 24, Ajman'
                );
        StoreSCS(1, 1, 5, 'm003732439', true, 'Handed over to Offer House Ent. for retail sales',
                'JLT, Dubai'
                );
        StoreProduct(6, "Weixi T 11", '2023 Main Release', 100, 6, 7,
            "xab3857x", //Automatically taken
            true, "Order given to outsourced factory Express in X province",
            "Shanghai, China"  //Automatically taken
        );
        StoreSCS(2, 7, 8, 'dfjhb7777', true, 'Shipped to Alibaba warehouse 201',
                'X Province, China'
                );
        addCompany("Iran Farmers' Union", "Saffron Farming Corporation");
        addCompany('Blackmores', 'Herb Packaging');
        StoreProduct(10, "Grade 1 Pure Saffron ", 'Negin & Sargol parts of stigma hand-picked',
            50, 9, 10,
            "12948738-435", //Automatically taken
            false, "Produce transporting to packaging venue",
            "Tehran, Iran"  //Automatically taken
        );
        StoreSCS(3, 10, 2, 'm00375638', true, 'Exporting 5kg of produce ie. 50 pieces globally',
                'Jebel Ali Port, Dubai'
                );
        StoreSCS(3, 2, 4,
                'm00375638', true,
                '25kg given to Madina', 'Jebel Ali Port, Dubai'
                );
        addCompany("xpharma", "sample for login testing");
    }
}
