import Foundation
import Combine

struct CatalogItem: Codable, Identifiable, Hashable {
    let id: String
    let name: String
    let source: String
    let lastVerified: String

    enum CodingKeys: String, CodingKey {
        case id, name, source
        case lastVerified = "last_verified"
    }
}

final class CatalogStore: ObservableObject {
    @Published private(set) var items: [CatalogItem] = []
    @Published var query = ""

    init() {
        guard let url = Bundle.main.url(forResource: "catalog", withExtension: "json", subdirectory: "Catalog"),
              let data = try? Data(contentsOf: url),
              let decoded = try? JSONDecoder().decode([CatalogItem].self, from: data) else { return }
        items = decoded
    }

    var filtered: [CatalogItem] {
        let value = query.folding(options: .diacriticInsensitive, locale: .current).lowercased()
        return items.filter { value.isEmpty || $0.name.folding(options: .diacriticInsensitive, locale: .current).lowercased().contains(value) }
    }
}
