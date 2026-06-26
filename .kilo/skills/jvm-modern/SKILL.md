---
name: jvm-modern
description: Especialista em Java 21+ e Kotlin backend moderno (Spring Boot 3 / Quarkus / Micronaut + JPA/Hibernate + JUnit 5 + Testcontainers). Cobre API REST, GraphQL, microservices reativos, batch, e deploy (Docker, GraalVM native, Kubernetes).
whenToUse: Use quando o usuario pedir "API Java", "backend Java", "Spring Boot", "Quarkus", "Micronaut", "Kotlin backend", "Ktor", "microservico Java", "JPA", "Hibernate". NAO use para .NET, Node, Python, Go, ou Rust.
---

# jvm-modern

## Filosofia

**JVM = ecossistema maduro, performance excelente, ferramentas top.** Java 21+ (virtual threads) e Kotlin tornam a JVM moderna. Use para enterprise apps, sistemas bancarios, batch processing, e qualquer coisa que precise de estabilidade absoluta.

## Stack Padrao (Java 21+ / 2026)

| Camada | Tecnologia | Justificativa |
|--------|------------|---------------|
| Linguagem | **Java 21+ (LTS)** OU **Kotlin 2.0+** | Java: virtual threads. Kotlin: conciso |
| Framework | **Spring Boot 3.3+** (default) / **Quarkus 3.x** / **Micronaut 4.x** | Spring = maduro; Quarkus = cloud-native |
| Reativo | **Spring WebFlux** / **Mutiny** (Quarkus) / **Coroutines** (Kotlin) | Para alta concorrencia |
| ORM | **Spring Data JPA + Hibernate 6** / **jOOQ** / **Exposed** (Kotlin) | JPA = padrao |
| Migrations | **Flyway** / **Liquibase** | Versionamento de schema |
| Validation | **Bean Validation (jakarta.validation)** | Built-in |
| Auth | **Spring Security + OAuth2 Resource Server** | Padrao enterprise |
| OpenAPI | **springdoc-openapi** | Gerado automatico |
| Testing | **JUnit 5 + Mockito + Testcontainers + AssertJ** | Padrao |
| Build | **Maven** (XML) OU **Gradle (Kotlin DSL)** | Gradle eh mais moderno |
| Lint/Format | **Spotless** + **Checkstyle** / **ktlint** | Format + lint |
| Logging | **Logback** (Spring) / **JBoss Logger** (Quarkus) | Estruturado |
| Monitoring | **Micrometer** + **Prometheus** + **Grafana** | Observabilidade |
| Deploy | **Docker**, **GraalVM native image**, **Kubernetes** | Multi-target |

## Decisoes de Arquitetura

### 1. Framework: Spring Boot vs Quarkus vs Micronaut
- **Spring Boot 3.3+** (recomendado 2026): ecossistema gigante, maduro, comunidade
- **Quarkus**: cloud-native, fast startup, GraalVM native, red hat
- **Micronaut**: compile-time DI, fast startup, similar ao Spring
- **Helidon**: Oracle, mas menor comunidade
- **Recomendacao**: Spring Boot para apps enterprise; Quarkus para cloud-native/Kubernetes

### 2. Linguagem: Java vs Kotlin
- **Java 21+** (LTS, virtual threads, pattern matching): padrao, mais devs
- **Kotlin 2.0+**: mais conciso, null safety, coroutines, interop 100% com Java
- **Recomendacao**: Kotlin para novos projetos (menos boilerplate); Java se equipe eh tradicional

### 3. Sync vs Reactive
- **Sync (Spring MVC + JPA)**: apps CRUD, simplicidade
- **Reactive (WebFlux + R2DBC)**: alta concorrencia, streaming
- **Virtual Threads (Java 21+)**: sync com concorrencia alta, sem complexidade de reativo
- **Recomendacao**: Virtual Threads (Java 21+) eh o sweet spot 2026

### 4. ORM: JPA/Hibernate vs jOOQ vs MyBatis
- **JPA + Hibernate** (default): padrao, repos, queries derived
- **jOOQ**: SQL-first, type-safe, gerado do schema
- **MyBatis**: SQL em XML, controle fino
- **Spring Data JPA**: repos automaticos, derived queries

### 5. Build Tool: Maven vs Gradle
- **Maven**: XML verboso, padrao legacy, estavel
- **Gradle (Kotlin DSL)**: mais rapido, mais expressivo, melhor para monorepo
- **Recomendacao**: Gradle para projetos novos; Maven se ja tem expertise


## Estrutura de Pastas (Spring Boot + Java 21)

```
/
├── src/
│   ├── main/
│   │   ├── java/com/example/myapp/
│   │   │   ├── MyAppApplication.java
│   │   │   ├── config/
│   │   │   ├── controller/
│   │   │   ├── service/
│   │   │   ├── repository/
│   │   │   ├── entity/
│   │   │   ├── dto/
│   │   │   ├── mapper/
│   │   │   ├── exception/
│   │   │   ├── security/
│   │   │   └── util/
│   │   └── resources/
│   │       ├── application.yml
│   │       ├── application-dev.yml
│   │       ├── application-prod.yml
│   │       ├── db/migration/
│   │       └── logback-spring.xml
│   └── test/java/com/example/myapp/
│       ├── controller/
│       ├── service/
│       ├── integration/
│       └── e2e/
├── docker/
├── .github/workflows/
├── .mvn/
├── mvnw, mvnw.cmd
├── pom.xml
└── README.md
```

## Setup Inicial (Spring Boot + Java 21)

```bash
curl https://start.spring.io/starter.zip   -d type=maven-project -d language=java -d bootVersion=3.3.0   -d baseDir=my-app -d groupId=com.example -d artifactId=my-app   -d name=my-app -d javaVersion=21   -d dependencies=web,data-jpa,postgresql,security,oauth2-resource-server,validation,actuator,flyway,testcontainers   -o my-app.zip
unzip my-app.zip && cd my-app
```

## Padroes Obrigatorios

- **Java 21+ LTS** (use virtual threads!)
- **Constructor injection** (NAO field injection)
- **Records** para DTOs (immutable, conciso)
- **Optional<T>** para retornos que podem ser ausentes
- **BigDecimal** para valores monetarios
- **ISO 8601** para datas (Instant, LocalDateTime)
- **Bean Validation** em todos DTOs
- **MapStruct** para mapping
- **Flyway/Liquibase** para migrations
- **Global exception handler** com @ControllerAdvice
- **API versionada**: `/api/v1/...`
- **OpenAPI** com springdoc
- **Tests**: @WebMvcTest + @DataJpaTest + @SpringBootTest + Testcontainers
- **SLF4J** para logging (NUNCA System.out)

## Anti-patterns

- Field injection (`@Autowired` em fields)
- `System.out.println` em producao
- `double` para valores monetarios
- `null` checks manuais (use `Optional`)
- Mutavel DTOs (use records)
- God services
- `@Transactional` em classes
- Hardcoded SQL strings
- Eager fetching excessivo (cause N+1)

## Exemplo: Spring Boot Controller + Service + Repository

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
@Tag(name = "Users")
public class UserController {
    private final UserService userService;

    @GetMapping
    public Page<UserDto> list(@PageableDefault(size = 20) Pageable pageable) {
        return userService.list(pageable);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserDto create(@Valid @RequestBody CreateUserRequest request) {
        return userService.create(request);
    }
}

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserService {
    private final UserRepository repository;
    private final UserMapper mapper;

    public Page<UserDto> list(Pageable pageable) {
        return repository.findAll(pageable).map(mapper::toDto);
    }

    @Transactional
    public UserDto create(CreateUserRequest request) {
        if (repository.existsByEmail(request.email())) {
            throw new EmailAlreadyExistsException(request.email());
        }
        User user = mapper.toEntity(request);
        user.setPassword(passwordEncoder.encode(request.password()));
        return mapper.toDto(repository.save(user));
    }
}
```

## Validacao

```bash
mvn clean verify                    # Build + tests
mvn spring-boot:run                 # Run
mvn test                            # Tests
mvn spotless:apply                  # Format
docker build -t my-app .            # Docker
```

## Comandos

```
/criar-api API de gestao de usuarios com Spring Boot + JPA + PostgreSQL
/criar-api microservico com Quarkus + Kotlin
/criar-projeto app Spring Boot com auth JWT + roles
```

## Output Esperado

Ao usar este skill, o agente deve produzir:

1. `pom.xml` ou `build.gradle.kts` com deps corretas
2. `mvnw` / `mvnw.cmd` + `.mvn/wrapper/`
3. `src/main/java/.../MyAppApplication.java`
4. `application.yml` + profiles
5. Entities JPA em `entity/`
6. Repositories em `repository/`
7. Services em `service/`
8. Controllers em `controller/`
9. DTOs (records) em `dto/`
10. Mappers (MapStruct) em `mapper/`
11. Exception handlers em `exception/`
12. Security config em `config/SecurityConfig.java`
13. Migrations em `resources/db/migration/`
14. Tests em `src/test/`
15. Dockerfile multi-stage
16. docker-compose.yml
17. README com setup, profiles, scripts
