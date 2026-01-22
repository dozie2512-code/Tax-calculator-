import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Single-file consolidated UK Tax Allowances model
 * Suitable for calculators, APIs, rule engines, or UI layers
 */
public final class UKTaxAllowances {

    private UKTaxAllowances() {}

    /* =========================
       Allowance Category Enum
       ========================= */
    public enum AllowanceCategory {
        PERSONAL,
        EMPLOYMENT,
        PENSION,
        SAVINGS_INVESTMENT,
        PROPERTY,
        BUSINESS,
        FAMILY,
        CHARITY,
        NATIONAL_INSURANCE,
        ADVANCED_INVESTMENT,
        INTERNATIONAL
    }

    /* =========================
       Tax Allowance Model
       ========================= */
    public record TaxAllowance(
            String code,
            String name,
            String description,
            AllowanceCategory category,
            double annualLimit,   // -1 = variable / uncapped
            boolean requiresClaim
    ) {}

    /* =========================
       Consolidated Allowances
       ========================= */
    public static final List<TaxAllowance> ALL = List.of(

        // PERSONAL
        new TaxAllowance("PA", "Personal Allowance",
                "Tax-free income threshold",
                AllowanceCategory.PERSONAL, 12_570, false),

        new TaxAllowance("MA", "Marriage Allowance",
                "Transfer unused allowance to spouse or civil partner",
                AllowanceCategory.PERSONAL, 1_260, true),

        new TaxAllowance("BPA", "Blind Person’s Allowance",
                "Additional allowance for visually impaired taxpayers",
                AllowanceCategory.PERSONAL, 2_870, true),

        // EMPLOYMENT
        new TaxAllowance("WFH", "Working From Home Allowance",
                "Flat-rate or actual home-working expenses",
                AllowanceCategory.EMPLOYMENT, 312, true),

        new TaxAllowance("MAR", "Mileage Allowance Relief",
                "Relief where employer pays below HMRC mileage rates",
                AllowanceCategory.EMPLOYMENT, -1, true),

        // PENSION
        new TaxAllowance("PEN", "Pension Contribution Relief",
                "Tax relief on pension contributions",
                AllowanceCategory.PENSION, 60_000, false),

        // SAVINGS & INVESTMENT
        new TaxAllowance("ISA", "ISA Allowance",
                "Tax-free savings, dividends, and capital gains",
                AllowanceCategory.SAVINGS_INVESTMENT, 20_000, false),

        new TaxAllowance("DIV", "Dividend Allowance",
                "Tax-free dividend income",
                AllowanceCategory.SAVINGS_INVESTMENT, 500, false),

        new TaxAllowance("CGT", "Capital Gains Allowance",
                "Annual capital gains exemption",
                AllowanceCategory.SAVINGS_INVESTMENT, 3_000, false),

        // PROPERTY
        new TaxAllowance("PIA", "Property Income Allowance",
                "Tax-free rental income",
                AllowanceCategory.PROPERTY, 1_000, false),

        new TaxAllowance("RAR", "Rent-a-Room Relief",
                "Tax-free income from letting a room in your home",
                AllowanceCategory.PROPERTY, 7_500, false),

        // BUSINESS
        new TaxAllowance("TRA", "Trading Allowance",
                "Tax-free trading income",
                AllowanceCategory.BUSINESS, 1_000, false),

        new TaxAllowance("AIA", "Annual Investment Allowance",
                "100% deduction for qualifying business equipment",
                AllowanceCategory.BUSINESS, 1_000_000, false),

        // FAMILY
        new TaxAllowance("TFC", "Tax-Free Childcare",
                "Government childcare top-up",
                AllowanceCategory.FAMILY, 2_000, true),

        // CHARITY
        new TaxAllowance("GA", "Gift Aid Relief",
                "Extends basic rate band for charitable donations",
                AllowanceCategory.CHARITY, -1, true),

        // NATIONAL INSURANCE
        new TaxAllowance("EA", "Employment Allowance",
                "Employer National Insurance reduction",
                AllowanceCategory.NATIONAL_INSURANCE, 5_000, true),

        // ADVANCED INVESTMENT
        new TaxAllowance("EIS", "Enterprise Investment Scheme",
                "30% income tax relief on qualifying investments",
                AllowanceCategory.ADVANCED_INVESTMENT, -1, true),

        new TaxAllowance("SEIS", "Seed Enterprise Investment Scheme",
                "50% income tax relief on early-stage investments",
                AllowanceCategory.ADVANCED_INVESTMENT, -1, true)
    );

    /* =========================
       Example Utility Methods
       ========================= */

    public static List<TaxAllowance> byCategory(AllowanceCategory category) {
        return ALL.stream()
                .filter(a -> a.category() == category)
                .toList();
    }

    public static Map<AllowanceCategory, List<TaxAllowance>> groupByCategory() {
        return ALL.stream()
                .collect(Collectors.groupingBy(TaxAllowance::category));
    }

    public static List<TaxAllowance> claimRequired() {
        return ALL.stream()
                .filter(TaxAllowance::requiresClaim)
                .toList();
    }

    /* =========================
       Example Main (optional)
       ========================= */
    public static void main(String[] args) {
        byCategory(AllowanceCategory.PERSONAL)
                .forEach(a -> System.out.println(a.name()));
    }
}
