"""Python program: Walmart weekly sales regression model."""

from app.walmart_regression_service import run_walmart_regression


def main() -> None:
    result = run_walmart_regression(refresh=True)
    print("Walmart regression model")
    print(f"Train period: {result['train_period']['from']} - {result['train_period']['to']}")
    print(f"Train rows: {result['train_rows']}")
    print(f"Test rows: {result['test_rows']}")
    print(f"MSE (test): {result['mse_test']}")
    print("\nCoefficients:")
    for item in result["coefficients"]:
        print(f"  {item['feature']}: {item['coefficient']}")
    print(f"  intercept: {result['intercept']}")
    print("\nCorrelation table:")
    for row in result["correlation_table"]:
        print(row)


if __name__ == "__main__":
    main()
