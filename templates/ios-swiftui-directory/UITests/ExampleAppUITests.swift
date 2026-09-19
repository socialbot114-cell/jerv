import XCTest

final class ExampleAppUITests: XCTestCase {
    func testLaunch() {
        let app = XCUIApplication()
        app.launch()
        XCTAssertTrue(app.exists)
    }
}
